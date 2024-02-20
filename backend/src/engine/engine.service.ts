import { Injectable } from '@nestjs/common';
import { CreateEngineDto } from './dto/create-engine.dto';
import { UpdateEngineDto } from './dto/update-engine.dto';
import { Engine } from './entities/engine.entity';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { HttpService } from '@nestjs/axios';
import { StartScanDto } from './dto/start-scan.dto';
import { EngineType } from './entities/engine-type.entity';
import { Socket, io } from 'socket.io-client';
import { WorkflowService } from 'src/workflow/workflow.service';

export interface EngineData {
  engine: string;
  options: any;
  status: string;
  need_assets: boolean;
  example_response: any;
}

export interface EngineWithData extends Engine {
  data: EngineData;
}

export interface Scan {
  results: any[];
}

@Injectable()
export class EngineService {
  private clients: Socket[] = [];

  constructor(
    @InjectRepository(Engine)
    private enginesRepository: Repository<Engine>,
    @InjectRepository(EngineType)
    private engineTypeRepository: Repository<EngineType>,
    private readonly httpService: HttpService,
    private readonly workflowService: WorkflowService,
  ) {
    this.resetSockets();
  }

  private async resetSockets() {
    for (const client of this.clients) {
      client.disconnect();
    }
    this.clients = [];
    for (const engine of await this.findAll()) {
      this.establishSocket(engine);
    }
  }

  private establishSocket(engine: Engine) {
    const client = io(`${engine.url}`);
    this.clients.push(client);
    client.on('connect', () => {
      console.log(`Engine ${engine.url} is connected`);
    });
    client.on('scan-finished', (data) => {
      this.iterateWorkflowsFromEndedScan(engine, data);
    });
    this.clients.push(client);
  }

  private async iterateWorkflowsFromEndedScan(engine: Engine, scan_id: any) {
    const scan = await this.getEngineScan(engine, scan_id);
    const type = await this.getEngineData(engine);

    const workflows = await this.workflowService.findForEngineSource(
      type.engine,
    );
    for (const workflow of workflows) {
      const assets = [];
      const options = {};
      // Need assets
      // if (workflow.engineTarget.need_assets) {
      for (const result of scan.results) {
        assets.push(...updateOutput(result, workflow.extractAssets));
      }

      // }
      // Extract options
      if (workflow.extractOptions) {
        for (const option in workflow.extractOptions) {
          if (!workflow.extractOptions[option].extracted) {
            options[option] = workflow.extractOptions[option].value;
          } else {
            options[option] = [];
            for (const result of scan.results) {
              options[option].push(
                ...updateOutput(result, workflow.extractOptions[option].value),
              );
            }
          }
        }
      }

      // Match conditions
      let flag = true;
      if (workflow.conditions) {
        for (const condition of (workflow as any).conditions) {
          if (checkCondition(condition, scan) == false) {
            console.log('condition failed', condition);
            flag = false;
          }
        }
      }
      if (!flag) {
        continue;
      }

      try {
        console.log(
          'Start workflows with assets',
          assets.flat(),
          'and options',
          options,
        );
        return await this.findAvailableEngineAndStartScan(
          workflow.engineTarget.name,
          {
            assets: assets.flat(),
            options: options,
          },
        );
      } catch (error) {
        console.error('Workflow failed: ', error.message);
      }
    }
  }

  public async create(createEngineDto: CreateEngineDto) {
    const engine = await this.enginesRepository.save({
      url: removeTrailingSlash(createEngineDto.url),
    });
    this.establishSocket(engine);
    return engine;
  }

  public async getTypes() {
    return this.engineTypeRepository.find();
  }

  private async getEngineData(engine: Engine) {
    try {
      const engineStatus = await this.httpService
        .get<EngineData>(engine.url)
        .toPromise();
      const engineType = await this.engineTypeRepository.findOneBy({
        name: engineStatus.data.engine,
      });
      if (engineType) {
        if (
          JSON.stringify(engineType.options).length !=
            JSON.stringify(engineStatus.data.options).length ||
          JSON.stringify(engineType.reponse).length !=
            JSON.stringify(engineStatus.data.example_response).length ||
          engineType.need_assets != engineStatus.data.need_assets
        ) {
          engineType.options = engineStatus.data.options;
          engineType.reponse = engineStatus.data.example_response;
          engineType.need_assets = engineStatus.data.need_assets;
          engineType.save();
        }
      } else {
        this.engineTypeRepository.save({
          name: engineStatus.data.engine,
          options: engineStatus.data.options,
          reponse: engineStatus.data.example_response,
          need_assets: engineStatus.data.need_assets,
        });
      }
      return engineStatus.data;
    } catch (error) {
      return null;
    }
  }

  private async getEngineScans(engine: Engine) {
    try {
      const req = await this.httpService.get(`${engine.url}/scans`).toPromise();
      return req.data;
    } catch (error) {
      return null;
    }
  }

  private async getEngineScan(engine: Engine, scanId: string) {
    try {
      const req = await this.httpService
        .get<Scan>(`${engine.url}/scans/${scanId}`)
        .toPromise();
      return req.data;
    } catch (error) {
      return null;
    }
  }

  public async getScans(engineId: string) {
    const engine = await this.findOne(engineId);
    return this.getEngineScans(engine);
  }

  public async getScan(engineId: string, scanId: string) {
    const engine = await this.findOne(engineId);
    return this.getEngineScan(engine, scanId);
  }

  private async sendScanToEngine(engine: Engine, payload: StartScanDto) {
    try {
      const req = await this.httpService
        .post(`${engine.url}/start`, {
          assets: {
            values: payload.assets,
          },
          options: payload.options,
        })
        .toPromise();
      return req.data;
    } catch (error) {
      return null;
    }
  }

  public async startScan(engineId: string, payload: StartScanDto) {
    const engine = await this.findOne(engineId);
    return this.sendScanToEngine(engine, payload);
  }

  public async findEnginesByName(name: string): Promise<EngineWithData[]> {
    const engines = await this.findAll();
    const result = [];
    for (const engine of engines) {
      const data = await this.getEngineData(engine);
      if (data?.engine == name) result.push({ ...engine, data });
    }
    return result;
  }

  public async findAvailableEngineAndStartScan(
    engineName: string,
    payload: StartScanDto,
  ) {
    const engines = await this.findEnginesByName(engineName);
    if (!engines[0]) {
      throw new Error('No engine available');
    }
    return await this.sendScanToEngine(engines[0], payload);
  }

  public async findWithData(): Promise<EngineWithData> {
    const engines = await this.findAll();
    for (const engine of engines) {
      const data = await this.getEngineData(engine);
      if (data) (engine as any).data = data;
    }
    return engines as any;
  }

  public findAll() {
    return this.enginesRepository.find();
  }

  public findOne(id: string) {
    return this.enginesRepository.findOneBy({ id });
  }

  public update(id: string, updateEngineDto: UpdateEngineDto) {
    return `This action updates a #${id} engine`;
  }

  public async remove(id: string) {
    await this.enginesRepository.delete(id);
    return true;
  }
}

function checkCondition(condition, scan) {
  // Equal
  condition.toMatch = [];
  for (const result of scan.results) {
    condition.toMatch.push(...updateOutput(result, condition.jsonToMatch));
  }
  if (condition.matcher == 0) {
    for (const toMatch of condition.toMatch) {
      if (toMatch == condition.string) {
        return true;
      }
    }
  }
  return false;
}

function updateOutput(scanObject, search) {
  let recursiveObjects = [scanObject];
  for (const index in search) {
    // console.log(index, pickeds.value[index].key, recursiveObjects);
    recursiveObjects = findValues(
      recursiveObjects,
      search[index],
      search[parseInt(index) + 1],
    );
  }
  return recursiveObjects;
}

function findValues(objects: any, picked: any, nextPicked: any | null) {
  let values = [];
  for (const object of objects) {
    if (picked.all) {
      for (const value of object) {
        if (!nextPicked || !value[nextPicked.key]) return objects;
        values.push(value[nextPicked.key]);
      }
    } else {
      if (!object[picked.key]) {
        if (!nextPicked || !object[nextPicked.key]) return objects;
        values.push(object[nextPicked.key]);
      } else {
        if (object[picked.key]) values.push(object[picked.key]);
      }
    }
  }
  return values;
}

function removeTrailingSlash(url) {
  if (url.endsWith('/')) {
    return url.slice(0, -1);
  }
  return url;
}

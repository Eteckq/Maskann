import { Injectable } from '@nestjs/common';
import { CreateScandefDto } from './dto/create-scandef.dto';
import { UpdateScandefDto } from './dto/update-scandef.dto';
import { ScanDef } from './entities/scandef.entity';
import { Repository } from 'typeorm';
import { InjectRepository } from '@nestjs/typeorm';
import { EngineService } from 'src/engine/engine.service';

@Injectable()
export class ScandefService {
  constructor(
    @InjectRepository(ScanDef)
    private repository: Repository<ScanDef>,
    private readonly engineService: EngineService,
  ) {}

  async startScan(scanDefId: string, assets: string[]) {
    const scanDef = await this.findOne(scanDefId);
    const engines = await this.engineService.findEnginesByName(
      scanDef.engineName,
    );
    const usingEngine = engines[0];

    return {
      engine: usingEngine.id,
      ...(await this.engineService.startScan(usingEngine.id, {
        assets,
        options: scanDef.options,
      })),
    };
  }

  create(createScandefDto: CreateScandefDto) {
    return this.repository.save(createScandefDto);
  }

  findAll() {
    return this.repository.find();
  }

  findOne(id: string) {
    return this.repository.findOneBy({ id: id });
  }

  update(id: string, updateScandefDto: UpdateScandefDto) {
    return `This action updates a #${id} scandef`;
  }

  async remove(id: string) {
    await this.repository.delete(id);
    return true;
  }
}

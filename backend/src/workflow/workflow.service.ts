import { Injectable } from '@nestjs/common';
import { CreateWorkflowDto } from './dto/create-workflow.dto';
import { UpdateWorkflowDto } from './dto/update-workflow.dto';
import { Workflow } from './entities/workflow.entity';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';

@Injectable()
export class WorkflowService {
  constructor(
    @InjectRepository(Workflow)
    private repository: Repository<Workflow>,
  ) {}

  create(createWorkflowDto: CreateWorkflowDto) {
    return this.repository.save(createWorkflowDto);
  }

  findAll() {
    return this.repository.find({
      relations: ['engineOrigin', 'engineTarget', 'scandefTarget'],
    });
  }

  findOne(id: string) {
    return this.repository.findOne({
      where: { id: id },
      relations: ['engineOrigin', 'engineTarget', 'scandefTarget'],
    });
  }

  update(id: string, updateWorkflowDto: UpdateWorkflowDto) {
    return `This action updates a #${id} workflow`;
  }

  remove(id: string) {
    return this.repository.delete(id);
  }

  async findForEngineSource(engineType: string) {
    return this.repository.find({
      where: {
        engineOrigin: {
          name: engineType,
        },
      },
      relations: ['engineOrigin', 'engineTarget', 'scandefTarget'],
    });
  }
}

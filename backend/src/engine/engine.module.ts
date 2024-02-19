import { Module } from '@nestjs/common';
import { EngineService } from './engine.service';
import { EngineController } from './engine.controller';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Engine } from './entities/engine.entity';
import { HttpModule } from '@nestjs/axios';
import { EngineType } from './entities/engine-type.entity';
import { WorkflowModule } from 'src/workflow/workflow.module';

@Module({
  imports: [
    TypeOrmModule.forFeature([Engine, EngineType]),
    HttpModule,
    WorkflowModule,
  ],
  controllers: [EngineController],
  providers: [EngineService],
  exports: [EngineService],
})
export class EngineModule {}

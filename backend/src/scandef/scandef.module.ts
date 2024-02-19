import { Module } from '@nestjs/common';
import { ScandefService } from './scandef.service';
import { ScandefController } from './scandef.controller';
import { ScanDef } from './entities/scandef.entity';
import { TypeOrmModule } from '@nestjs/typeorm';
import { EngineModule } from 'src/engine/engine.module';

@Module({
  imports: [TypeOrmModule.forFeature([ScanDef]), EngineModule],
  controllers: [ScandefController],
  providers: [ScandefService],
})
export class ScandefModule {}

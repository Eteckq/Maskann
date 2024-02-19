import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
} from '@nestjs/common';
import { EngineService } from './engine.service';
import { CreateEngineDto } from './dto/create-engine.dto';
import { UpdateEngineDto } from './dto/update-engine.dto';
import { StartScanDto } from './dto/start-scan.dto';
import { ApiTags } from '@nestjs/swagger';

@Controller('engine')
@ApiTags('Engines')
export class EngineController {
  constructor(private readonly engineService: EngineService) {}

  @Post()
  create(@Body() createEngineDto: CreateEngineDto) {
    return this.engineService.create(createEngineDto);
  }

  @Post(':engine_id/start')
  startScan(
    @Param('engine_id') engineId: string,
    @Body() payload: StartScanDto,
  ) {
    return this.engineService.startScan(engineId, payload);
  }

  @Get('types')
  getEngineTypes() {
    return this.engineService.getTypes();
  }

  @Get(':engine_id/scans')
  getScans(@Param('engine_id') engineId: string) {
    return this.engineService.getScans(engineId);
  }

  @Get(':engine_id/scans/:scan_id')
  getScan(
    @Param('engine_id') engineId: string,
    @Param('scan_id') scanId: string,
  ) {
    return this.engineService.getScan(engineId, scanId);
  }

  @Get()
  findWithStatus() {
    return this.engineService.findWithData();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.engineService.findOne(id);
  }

  @Patch(':id')
  update(@Param('id') id: string, @Body() updateEngineDto: UpdateEngineDto) {
    return this.engineService.update(id, updateEngineDto);
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.engineService.remove(id);
  }
}

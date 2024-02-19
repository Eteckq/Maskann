import { EngineType } from 'src/engine/entities/engine-type.entity';

export class CreateWorkflowDto {
  engineOrigin: EngineType;
  engineTarget: EngineType;
  conditions: JSON;
  extract: JSON;
}

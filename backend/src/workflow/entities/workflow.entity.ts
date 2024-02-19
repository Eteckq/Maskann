import { EngineType } from 'src/engine/entities/engine-type.entity';
import { ScanDef } from 'src/scandef/entities/scandef.entity';
import {
  Entity,
  Column,
  PrimaryGeneratedColumn,
  BaseEntity,
  ManyToOne,
} from 'typeorm';

@Entity()
export class Workflow extends BaseEntity {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @ManyToOne(() => EngineType)
  engineOrigin: EngineType;

  @ManyToOne(() => EngineType, { nullable: true })
  engineTarget: EngineType;

  @ManyToOne(() => ScanDef, { nullable: true })
  scandefTarget: ScanDef;

  @Column('json', { nullable: true })
  conditions: JSON;

  @Column('json')
  extractAssets: JSON;

  @Column('json')
  extractOptions: JSON;
}

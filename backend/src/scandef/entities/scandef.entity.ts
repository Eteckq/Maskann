import { Entity, Column, PrimaryGeneratedColumn, BaseEntity } from 'typeorm';

@Entity()
export class ScanDef extends BaseEntity {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  engineName: string;

  @Column('json')
  options: JSON;
}

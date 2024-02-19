import { Entity, Column, PrimaryGeneratedColumn, BaseEntity } from 'typeorm';

@Entity()
export class Engine extends BaseEntity {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  url: string;
}

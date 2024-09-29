import { IsNotEmpty, IsArray } from "class-validator";

export class RowDTO {
  @IsArray()
  @IsNotEmpty()
  row!: any[];
}

export class TableDTO {
  @IsNotEmpty()
  @IsArray()
  rows!: RowDTO[];
}

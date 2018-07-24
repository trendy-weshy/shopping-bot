import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChatbarComponent } from './chatbar.component';
import { SharedModule } from '../shared/shared.module';

@NgModule({
  imports: [
    CommonModule,
    SharedModule
  ],
  declarations: [
    ChatbarComponent
  ],
  exports: [
    ChatbarComponent
  ]
})
export class ChatBarModule { }

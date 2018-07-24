import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ShoppingProductsComponent } from './shopping-products/shopping-products.component';
import { SharedModule } from '../shared/shared.module';

@NgModule({
  imports: [
    CommonModule,
    SharedModule
  ],
  declarations: [ShoppingProductsComponent],
  exports: [ShoppingProductsComponent]
})
export class AppPagesModule { }

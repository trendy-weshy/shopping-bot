import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SidebarModuleRoutingModule } from './sidebar-module-routing.module';
import { OverlayContainer } from '@angular/cdk/overlay';
import { SharedModule } from '../shared/shared.module';
import { SidebarTabsComponent } from './sidebar-tabs/sidebar-tabs.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    SidebarModuleRoutingModule
  ],
  declarations: [SidebarTabsComponent],
  exports: [
    SidebarTabsComponent
  ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class SidebarModule {
  constructor(overlayContainer: OverlayContainer) {
    overlayContainer.getContainerElement().classList.add('eComm-dark-theme');
  }
}

import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { StoreModule } from '@ngrx/store';
import { StoreRouterConnectingModule, routerReducer } from '@ngrx/router-store';
import { devStorePlugins } from './store/dev';
import { UIReducer } from './store/reducers/ui';
import { AppState } from './store/interfaces';
import { EffectsModule } from '@ngrx/effects';
import { RouterEffects } from './store/effects/router';
import { getIntialState } from './store/default';

import { NgProgressModule } from '@ngx-progressbar/core';
import { NgProgressRouterModule } from '@ngx-progressbar/router';
import { NgProgressHttpModule } from '@ngx-progressbar/http';

import { MatSidenavModule } from '@angular/material/sidenav';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { SharedModule } from './shared/shared.module';
import { SidebarModule } from './sidebar-module/sidebar.module';
import { TopbarComponent } from './topbar/topbar.component';
import { AppPagesModule } from './pages/app-pages.module';
import { ChatBarModule } from './chatbar/chat-bar.module';

@NgModule({
  declarations: [
    AppComponent,
    TopbarComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    StoreModule.forRoot<AppState>({
      router: routerReducer,
      ui: UIReducer
    },
    {
      initialState: getIntialState
    }),
    StoreRouterConnectingModule.forRoot({
      stateKey: 'router',
    }),
    ...devStorePlugins,
    EffectsModule.forRoot([
      RouterEffects
    ]),
    NgProgressModule.forRoot(),
    NgProgressHttpModule,
    NgProgressRouterModule,
    AppRoutingModule,
    SharedModule,
    MatSidenavModule,
    SidebarModule,
    AppPagesModule,
    ChatBarModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

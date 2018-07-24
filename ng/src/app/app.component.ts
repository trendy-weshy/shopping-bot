import { Component, OnInit, OnDestroy, ViewChild } from '@angular/core';
import { BreakpointObserver, Breakpoints, BreakpointState } from '@angular/cdk/layout';
import { MatDrawer } from '@angular/material';
import { Observable } from 'rxjs/internal/Observable';
import { Subscription } from 'rxjs/internal/Subscription';
import { Store, select } from '@ngrx/store';
import { AppState, UIState } from './store/interfaces';
import { getUISidebarState } from './store/selectors';
import { ToggleSidebar, DefaultSidebar, ChangeSidebarMode, UpdateDevice } from './store/actions/ui';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, OnDestroy {

  tablet$: Observable<BreakpointState>;
  mobile$: Observable<BreakpointState>;
  desktop$: Observable<BreakpointState>;

  ui$: Observable<UIState>;

  tabletSubscription: Subscription;
  mobileSubscription: Subscription;
  desktopSubscription: Subscription;

  constructor(breakpointObserver: BreakpointObserver, private _store: Store<AppState>) {
    this.tablet$ = breakpointObserver.observe(['(max-width: 769px)']);
    this.mobile$ = breakpointObserver.observe([Breakpoints.XSmall]);
    this.desktop$ = breakpointObserver.observe([Breakpoints.Large]);

    this.ui$ = _store.pipe(select('ui'));
  }

  ngOnInit() {

    this.checkIsDesktop();
    this.checkIsTablet();
    this.checkIsMobile();

  }

  ngOnDestroy() {
    if (this.mobileSubscription) {
      this.mobileSubscription.unsubscribe();
    }
    if (this.tabletSubscription) {
      this.tabletSubscription.unsubscribe();
    }
    if (this.desktopSubscription) {
      this.desktopSubscription.unsubscribe();
    }
  }

  checkIsDesktop() {
    this.desktopSubscription = this.desktop$.subscribe(
      ({ matches }) => {

        if (matches) {
          this._store.dispatch(new DefaultSidebar());
          this._store.dispatch(new UpdateDevice('desktop'));
        }

      }
    );
  }

  checkIsTablet() {
    this.tabletSubscription = this.tablet$.subscribe(
      ({ matches }) => {

        if (matches) {
          this._store.dispatch(new ChangeSidebarMode({ mode: 'over', backdrop: true, opened: false }));
          this._store.dispatch(new UpdateDevice('tablet'));
        }

      }
    );
  }

  checkIsMobile() {
    this.mobileSubscription = this.mobile$.subscribe(
      ({ matches }) => {

        if (matches) {
          this._store.dispatch(new ToggleSidebar());
          this._store.dispatch(new ChangeSidebarMode({ mode: 'over', backdrop: true, opened: false }));
          this._store.dispatch(new UpdateDevice('mobile'));
        }

      }
    );
  }

  toggleSidebar() {
    this._store.dispatch(new ToggleSidebar());
  }

}

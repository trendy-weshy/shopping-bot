import { Component, OnInit, OnDestroy} from '@angular/core';
import { AppState, UIState } from '../store/interfaces';
import { Store, select } from '@ngrx/store';
import { ToggleSidebar } from '../store/actions/ui';
import { Observable } from 'rxjs/internal/Observable';
import { Breakpoints, BreakpointObserver } from '@angular/cdk/layout';
import { Subscription } from 'rxjs/internal/Subscription';

@Component({
  selector: 'app-topbar',
  templateUrl: './topbar.component.html',
  styleUrls: ['./topbar.component.scss']
})
export class TopbarComponent implements OnInit, OnDestroy {

  ui$: Observable<UIState>;
  xSmallDevice: Subscription;
  smallDevice: Subscription;

  isSmallDevice: boolean;
  isXSmallDevice: boolean;

  constructor(private _store: Store<AppState>, breakpointObserver: BreakpointObserver) {
    this.ui$ = _store.pipe(select('ui'));

    this.smallDevice =  breakpointObserver.observe([ '(max-width: 400px)' ]).subscribe(({ matches }) => this.isSmallDevice = matches);
    this.xSmallDevice =  breakpointObserver.observe([ '(max-width: 320px)' ]).subscribe(({ matches }) => this.isXSmallDevice = matches);
  }

  ngOnInit() { }

  ngOnDestroy() {
    if (this.xSmallDevice) {
      this.xSmallDevice.unsubscribe();
    }
    if (this.smallDevice) {
      this.smallDevice.unsubscribe();
    }
  }

  toggleSidebar() {
    this._store.dispatch(new ToggleSidebar());
  }

}

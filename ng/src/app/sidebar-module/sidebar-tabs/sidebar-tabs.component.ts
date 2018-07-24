import { Component, OnInit } from '@angular/core';
import { UIState, AppState } from '../../store/interfaces';
import { Observable } from 'rxjs/internal/Observable';
import { Store, select } from '@ngrx/store';
import { ToggleSidebar } from '../../store/actions/ui';

@Component({
  selector: 'app-sidebar-tabs',
  templateUrl: './sidebar-tabs.component.html',
  styleUrls: ['./sidebar-tabs.component.scss']
})
export class SidebarTabsComponent implements OnInit {

  ui$: Observable<UIState>;

  constructor(private _store: Store<AppState>) {
    this.ui$ = this._store.pipe(select('ui'));
  }

  ngOnInit() {
  }

  toggleSidebar() {
    this._store.dispatch(new ToggleSidebar());
  }

}

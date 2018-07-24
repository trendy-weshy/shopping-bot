import { Component, OnInit } from '@angular/core';
import { AppState, UIState } from '../../store/interfaces';
import { Store, select } from '@ngrx/store';
import { Observable } from 'rxjs/internal/Observable';

@Component({
  selector: 'app-shopping-products',
  templateUrl: './shopping-products.component.html',
  styleUrls: ['./shopping-products.component.scss']
})
export class ShoppingProductsComponent implements OnInit {
  ui$: Observable<UIState>;

  constructor(private _store: Store<AppState>) {
    this.ui$ = _store.pipe(select('ui'));
  }

  ngOnInit() {
  }

}

/**
 * Redux State Interfaces
 */

import { RouterReducerState } from '@ngrx/router-store';

export interface UIState {
  sidebar: {
    opened: boolean;
    mode: string;
    backdrop: boolean;
  };
  device: string;
}

/**
 * Main Redux State
 */
export interface AppState {
  ui: UIState;
  router: RouterReducerState;
}

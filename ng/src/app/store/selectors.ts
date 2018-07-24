/**
 * Redux store selector
 */

import { createSelector } from '@ngrx/store';

export const getUIState = state => state.ui;
export const getUISidebarState = createSelector(getUIState, state => state.sidebar);

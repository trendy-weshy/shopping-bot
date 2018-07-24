/**
 * UI Redux Actions
 */

import { Action } from '@ngrx/store';

export const TOGGLE_SIDEBAR = '[UI] Toggle Sidebar';
export const DEFAULT_SIDEBAR = '[UI] Default Sidebar';
export const CHANGE_SIDEBAR_MODE = '[UI] Change Sidebar mode';
export const UPDATE_DEVICE = '[UI] Update Device Type';

export type UIActions = ToggleSidebar | DefaultSidebar | ChangeSidebarMode | UpdateDevice;

export class ToggleSidebar implements Action {
  readonly type = TOGGLE_SIDEBAR;
}

export class DefaultSidebar implements Action {
  readonly type = DEFAULT_SIDEBAR;
}

export class ChangeSidebarMode implements Action {
  readonly type = CHANGE_SIDEBAR_MODE;

  constructor(public payload: { mode: 'side' | 'push' | 'over';  backdrop?: boolean; opened?: boolean; }) {}
}

export class UpdateDevice implements Action {
  readonly type = UPDATE_DEVICE;

  constructor(public payload: 'desktop' | 'tablet' | 'mobile') {}
}

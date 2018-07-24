/**
 * Contains the UI state for the application
 */

import { UIState } from '../interfaces';
import { UIActions, TOGGLE_SIDEBAR, DEFAULT_SIDEBAR, CHANGE_SIDEBAR_MODE, UPDATE_DEVICE } from '../actions/ui';

export const UIDefaultState = {
  sidebar: {
    opened: true,
    mode: 'side',
    backdrop: false
  },
  device: 'desktop'
};

export function UIReducer(state: UIState, action: UIActions) {

  switch (action.type) {

    case TOGGLE_SIDEBAR:
      return Object.assign({}, state, { sidebar: { ...state.sidebar, opened: !state.sidebar.opened } });

    case DEFAULT_SIDEBAR:
      return Object.assign({}, state, { sidebar: { mode: 'side', opened: true, device: 'desktop', backdrop: false } });

    case CHANGE_SIDEBAR_MODE:
      return Object.assign({}, state, { sidebar: { ...state.sidebar, ...action.payload } });

    case UPDATE_DEVICE:
    return Object.assign({}, state, { device: action.payload });

    default:
      return state;

  }

}

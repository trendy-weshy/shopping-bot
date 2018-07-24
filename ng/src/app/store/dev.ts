import { environment } from '../../environments/environment';
import { StoreDevtoolsModule } from '@ngrx/store-devtools';
import { StoreLogMonitorModule, useLogMonitor } from '@ngrx/store-log-monitor';

export const devStorePlugins = (!environment.production)
?
[
  StoreDevtoolsModule.instrument({ monitor: useLogMonitor({ visible: true, position: 'right' }) }),
  StoreLogMonitorModule
]
:
[];

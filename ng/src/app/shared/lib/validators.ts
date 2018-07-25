import * as moment from 'moment';
import { isMobilePhone, isEmail } from 'validator';
import { isNil, isEmpty, isDate, isNumber } from 'lodash';
import { FormControl, FormGroup } from '@angular/forms';

export class CustomValidator {

  static isPhone(control: FormControl): any {
    return (!isEmpty(control.value) && !isMobilePhone(control.value, 'any')) ?
      { 'phone': true } : null;
  }

  static isEmail(control: FormControl): any {
    return !isEmpty(control.value) && !isEmail(control.value) ? { 'email': true } : null;
  }

  static passwordMatch(g: FormGroup, passKey: string): any {
    return (control: FormControl) => control.value === g.get(passKey).value ? null : { 'mismatch': true };
  }

  static isDate(control: FormControl): any {
    return !isEmpty(control.value) && !moment(control.value).isValid() ? { 'date': true } : null;
  }

  static isNumeric(control: FormControl) {
    return !isEmpty(control.value) && !isNumber(control.value) ? { 'numeric': true } : null;
  }
}

import {reactive} from 'vue';
//TEST 
let test_data = [
{id:1, text_f:'Быстрый собака ведет тихо. first', number_f:949398, ts_f:'2006-01-17T18:25:52', bool_f: true, row_info:'kek'},
{id:2, text_f:'Быстрый город бежит медленно.', number_f:-88376, ts_f:'2075-10-19T06:57:55', bool_f: true, row_info:'kek'},
{id:3, text_f:'Умный дом читает тихо.', number_f:-689484, ts_f:'2035-09-28T02:27:01', bool_f: true, row_info:'kek'},
{id:4, text_f:'Новый дом смотрит далеко.', number_f:-716125, ts_f:'1971-03-11T05:25:39', bool_f: true, row_info:'kek'},
{id:5, text_f:'Быстрый кошка строит медленно.', number_f:-737547, ts_f:'2048-12-16T16:12:39', bool_f: true, row_info:'kek'},
{id:6, text_f:'Умный собака играет далеко.', number_f:843126, ts_f:'2033-11-27T11:06:40', bool_f: true, row_info:'kek'},
{id:7, text_f:'Большой собака спит медленно.', number_f:-922272, ts_f:'1988-02-07T20:50:39', bool_f: true, row_info:'kekhhhjkjhkjhkhkhkjhkjhkjhkjhkjhkjhkjhkjhkjhkjhkjhkjhkjghuigiiugigygu999'},
{id:8, text_f:'Умный ребенок спит далеко.', number_f:808076, ts_f:'2021-10-23T01:18:32', bool_f: true, row_info:'kek'},
{id:9, text_f:'Новый город бежит быстро.', number_f:-984978, ts_f:'1994-09-28T21:43:34', bool_f: true, row_info:'kek'},
{id:10, text_f:'Старый кошка делает близко. last', number_f:180423, ts_f:'2031-01-19T17:26:51', bool_f: true, row_info:'kek'}
]
export let data = [];
for (let i=0; i<1000; i++){
  let row = Object.assign({}, test_data[Math.floor(Math.random() * test_data.length)]);
  row.id=i;
  data.push(row);
}


// Количество отображаемых строк (скользящее окно)
export let VIEW_CHUNK = 100;

// Пришлось сюда перенести реактивное состояние
// так как тут потребуется проверять from to при обновлении записи из EventSource 
export const scroll_r = reactive({
  last_scroll: 0,
  last_scroll_max: 0,
  from: 0,
  to: VIEW_CHUNK
});
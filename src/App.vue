<script setup>
import {ref, useTemplateRef, onMounted, computed} from 'vue';

let data = [
{id:1, text_f:'Быстрый собака ведет тихо.', number_f:949398, ts_f:'2006-01-17T18:25:52', bool_f: true, row_info:'kek'},
{id:2, text_f:'Быстрый город бежит медленно.', number_f:-88376, ts_f:'2075-10-19T06:57:55', bool_f: true, row_info:'kek'},
{id:3, text_f:'Умный дом читает тихо.', number_f:-689484, ts_f:'2035-09-28T02:27:01', bool_f: true, row_info:'kek'},
{id:4, text_f:'Новый дом смотрит далеко.', number_f:-716125, ts_f:'1971-03-11T05:25:39', bool_f: true, row_info:'kek'},
{id:5, text_f:'Быстрый кошка строит медленно.', number_f:-737547, ts_f:'2048-12-16T16:12:39', bool_f: true, row_info:'kek'},
{id:6, text_f:'Умный собака играет далеко.', number_f:843126, ts_f:'2033-11-27T11:06:40', bool_f: true, row_info:'kek'},
{id:7, text_f:'Большой собака спит медленно.', number_f:-922272, ts_f:'1988-02-07T20:50:39', bool_f: true, row_info:'kek'},
{id:8, text_f:'Умный ребенок спит далеко.', number_f:808076, ts_f:'2021-10-23T01:18:32', bool_f: true, row_info:'kek'},
{id:9, text_f:'Новый город бежит быстро.', number_f:-984978, ts_f:'1994-09-28T21:43:34', bool_f: true, row_info:'kek'},
{id:99999999, text_f:'Старый кошка делает близко.', number_f:180423, ts_f:'2031-01-19T17:26:51', bool_f: true, row_info:'kek'}
]

const dataView = ref([].concat(data, data, data));

onMounted(() => {
  // messagebox.value.focus()
})
</script>

<template>
  <div class="main">
    <div class="container">
      <h1>Тестовый стенд EventSource</h1>
      <form  action="javascript:void(0);"style="display: flex; flex-flow: row wrap; align-items: center;">
        <input type="number" placeholder="Количество записей" name="count" 
               style="vertical-align: middle; margin: 5px 10px 5px 0; padding: 10px; 
                      background-color: #fff; border: 1px solid #ddd;" />
        <button style="padding: 10px 20px; background-color: #266639ff; 
                       border: 1px solid #ddd; color: white;">Добавить</button>
        <button style="padding: 10px 20px; background-color: #912e2eff; 
                       border: 1px solid #ddd; color: white;">Очистить БД</button>
        <label style="margin: 5px 10px 5px 0;padding: 10px 20px;">Server Sent Events:</label>
        <button style="padding: 10px 20px; background-color: #009400ff; 
                       border: 1px solid #ddd; color: white;">Старт</button>
        <button style="padding: 10px 20px; background-color: #8b0035ff; 
                       border: 1px solid #ddd; color: white;">Остановка</button>
        <label style="margin: 5px 10px 5px 0;padding: 10px 20px;">Активно: загружено 100000 из 100000 записей</label>
    </form>
    <progress style="width:100%;" max="100" value="70"></progress>


    <h3>Запись</h3>
    <form action="javascript:void(0);" style="display: flex; flex-flow: row wrap; align-items: center;">
        <button style="padding: 10px 20px; background-color: #266639ff; 
                       border: 1px solid #ddd; color: white;">Добавить</button>
        <button style="padding: 10px 20px; background-color: #a36a00ff; 
                       border: 1px solid #ddd; color: white;">Изменить</button>
        <button style="padding: 10px 20px; background-color: #973535ff; 
                       border: 1px solid #ddd; color: white;">Удалить</button>
        <input type="number" placeholder="id" name="id"  disabled
               style="vertical-align: middle; margin: 2px 2px 0 0; padding: 10px; 
                      background-color: #fff; border: 1px solid #ddd;" />
        <input type="text" placeholder="text_f" name="text_f" 
               style="vertical-align: middle; margin: 2px 2px 0 0; padding: 10px; 
                      background-color: #fff; border: 1px solid #ddd;" />
        <input type="number" placeholder="number_f" name="number_f" 
               style="vertical-align: middle; margin: 2px 2px 0 0; padding: 10px; 
                      background-color: #fff; border: 1px solid #ddd;" />
        <input type="datetime-local" placeholder="ts_f" name="ts_f" 
               style="vertical-align: middle; margin: 2px 2px 0 0; padding: 10px; 
                      background-color: #fff; border: 1px solid #ddd;" />
        <label style="margin: 2px 2px 0 0;padding: 10px 20px;">bool_f</label>
        <input type="checkbox" placeholder="bool_f" name="bool_f" 
               style="vertical-align: middle; margin: 2px 2px 0 0; padding: 10px; 
                      background-color: #fff; border: 1px solid #ddd;" />
    </form>
    <h3>Фильтр</h3>
    <form action="javascript:void(0);" style="display: flex; flex-flow: row wrap; align-items: center;">
        <button style="padding: 10px 20px; background-color: #266639ff; 
                       border: 1px solid #ddd; color: white;">Применить</button>
        <button style="padding: 10px 20px; background-color: #a53b3bff; 
                       border: 1px solid #ddd; color: white;">Очистить</button>
        <input type="number" placeholder="id равно" name="id"
               style="vertical-align: middle; margin: 2px 2px 0 0; padding: 10px; 
                      background-color: #fff; border: 1px solid #ddd;" />
        <input type="text" placeholder="text_f содержит" name="text_f" 
               style="vertical-align: middle; margin: 2px 2px 0 0; padding: 10px; 
                      background-color: #fff; border: 1px solid #ddd;" />
        <select name="number_f_type" style="vertical-align: middle; margin: 2px 0 0 5px; padding: 10px; 
                      background-color: #fff; border: 1px solid #ddd;">
          <option value="равно" selected>равно</option>
          <option value="меньше">меньше</option>
          <option value="больше">больше</option>
        </select>
        <input type="number" placeholder="number_f" name="number_f" 
               style="vertical-align: middle; margin: 2px 2px 0 0; padding: 10px; 
                      background-color: #fff; border: 1px solid #ddd;" />
        <input type="datetime-local" placeholder="ts_f" name="ts_f" 
               style="vertical-align: middle; margin: 2px 2px 0 0; padding: 10px; 
                      background-color: #fff; border: 1px solid #ddd;" />
        <label style="margin: 2px 2px 0 0;padding: 10px 20px;">bool_f</label>
        <input type="checkbox" placeholder="bool_f" name="bool_f" 
               style="vertical-align: middle; margin: 2px 2px 0 0; padding: 10px; 
                      background-color: #fff; border: 1px solid #ddd;" />
        <input type="text" placeholder="row_info содержит" name="row_info" 
               style="vertical-align: middle; margin: 2px 2px 0 0; padding: 10px; 
                      background-color: #fff; border: 1px solid #ddd;" />
    </form>
    <div class="table_container">
      <table>
        <thead>
          <tr>
            <th>id</th>
            <th>text_f</th>
            <th>number_f</th>
            <th>ts_f</th>
            <th>bool_f</th>
            <th>row_info</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row  in dataView">
            <td>{{ row.id }}</td>
            <td>{{ row.text_f }}</td>
            <td>{{ row.number_f}}</td>
            <td>{{ row.ts_f }}</td>
            <td>{{ row.bool_f}}</td>
            <td>{{ row.row_info}}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <p>Показано с 0 по 0 строки</p>
    </div>
  </div>
</template>

<style scoped>
.main {
  margin:0;
  padding: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: #020024;
  background: linear-gradient(90deg, rgba(66, 62, 148, 1) 0%, rgba(49, 49, 141, 1) 35%, rgba(11, 118, 139, 1) 100%);
}
.container{
  width: 90vw;
  height: 90vh;
  padding: 10px;
  display: flex;
  flex-direction: column;
  background: #197370;
  background: linear-gradient(0deg, rgba(153, 145, 155, 1) 0%, rgba(209, 209, 209, 1) 100%);
  border: 2px solid #000000ff;
  border-radius: 10px 10px 10px 10px;
  box-shadow: 12px 18px 16px 8px rgba(34, 60, 80, 0.2);
}

.table_container{
  flex: 1;
  margin-top: 5px;
  border: 2px solid #000000ff;
  background: #a7a7a7ff;
  overflow-y: scroll;
}

progress {
  accent-color: #5a5a5aff; /* Sets the progress bar's fill color to blue */
}

button {
  border: 1px solid #5a5a5aff;
  border-radius: 5px 5px 5px 5px;
}

table{
  width: 100%;
  align-items:center;
  border-collapse: collapse;
}
th {
  position: sticky;
  top: 0;
  background: #a15252ff;
}
table, th, td {
  padding: 10px;
  border: 1px solid #3f3f3fff;
}
</style>

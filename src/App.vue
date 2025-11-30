<script setup>
import {ref, useTemplateRef, onMounted, reactive, defineModel} from 'vue';
import {VIEW_CHUNK, scroll_r, data, MessageBox} from '@/api';





const dataView = ref([]);

const dataSelect = {
  id: ref(),
  text_f: ref(),
  number_f:ref(),
  ts_f: ref(),
  bool_f: ref()
};

// const types ={
//   id: "int",
//   text_f: "str",
//   number_f:"int",
//   ts_f: "date",
//   bool_f: "bool",
//   row_info: "text",
// }
 
async function rowclick(row) {
  // console.log(row.tr);
  dataSelect.id.value = row.data.id;
  dataSelect.text_f.value = row.data.text_f;
  dataSelect.number_f.value = row.data.number_f;
  dataSelect.ts_f.value = row.data.ts_f;
  dataSelect.bool_f.value = row.data.bool_f;
  dataSelect.bool_f.checked = row.data.bool_f;
}

let __trootling = null;

function trottling(e){
  if (__trootling){
    clearTimeout(__trootling);
    __trootling = null;
  }
  __trootling = setTimeout(()=>scroll(e), 100);
}

async function scroll(e) {
  const current_scroll = e.target.scrollTop;
  const current_scroll_max = e.target.scrollHeight-e.target.clientHeight;
  const CHUNK = Math.round(VIEW_CHUNK/2);
  // чекаем скрол вниз до конца
  if(current_scroll >= current_scroll_max-1 && scroll_r.to < data.length){
    scroll_r.from+=CHUNK;
    scroll_r.to+=CHUNK;
    // Грамотно рассчитываем позицию скролла чтоб было максимально бесшовно
    // Половина всей высоты - половина отображаемого окна + высота одной записи)
    e.target.scrollTop = current_scroll_max/2 - e.target.clientHeight/2 + current_scroll_max/VIEW_CHUNK;
  }
  // чекаем скрол вверх до конца
  if(current_scroll <= 0 && scroll_r.from > 0  && scroll_r.from > 0){
    scroll_r.from-=CHUNK;
    scroll_r.to-=CHUNK;
    // Грамотно рассчитываем позицию скролла чтоб было максимально бесшовно
    // Половина всей высоты + половина отображаемого окна - высота одной записи)
    e.target.scrollTop = current_scroll_max/2 + e.target.clientHeight/2 - current_scroll_max/VIEW_CHUNK;
  }
  dataView.value = data.slice(scroll_r.from, scroll_r.to);
  // проставляем текущие позиции в реактив
  scroll_r.last_scroll = current_scroll;
  scroll_r.last_scroll_max = current_scroll_max;
}

onMounted(() => {
  dataView.value = data.slice(scroll_r.from, scroll_r.to);
})
</script>

<template>
  <dialog :ref="el=>MessageBox.dialog=el">
    <h2>{{MessageBox.header}}</h2>
    <p>{{MessageBox.message}}</p>

    <button type="button" @click="MessageBox.close()">
      Закрыть
    </button>
  </dialog>
  <div class="main">
    <div class="container">
      <h1>Тестовый стенд EventSource</h1>
      <form  action="javascript:void(0);"style="display: flex; flex-flow: row wrap; align-items: center;">
        <input type="number" placeholder="Количество записей" name="count" 
               style="vertical-align: middle; margin: 5px 10px 5px 0; padding: 10px; 
                      background-color: #fff; border: 1px solid #ddd;" />
        <button @click="MessageBox.show('test','test')"style="padding: 10px 20px; background-color: #266639ff; 
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
        <input :ref="(e)=>dataSelect.id=e" type="number" placeholder="id" name="id" disabled 
               style="vertical-align: middle; margin: 2px 2px 0 0; padding: 10px; 
                      background-color: #fff; border: 1px solid #ddd;" />
        <input :ref="(e)=>dataSelect.text_f=e" type="text" placeholder="text_f" name="text_f" 
               style="vertical-align: middle; margin: 2px 2px 0 0; padding: 10px; 
                      background-color: #fff; border: 1px solid #ddd;" />
        <input :ref="(e)=>dataSelect.number_f=e" type="number" placeholder="number_f" name="number_f" 
               style="vertical-align: middle; margin: 2px 2px 0 0; padding: 10px; 
                      background-color: #fff; border: 1px solid #ddd;" />
        <input :ref="(e)=>dataSelect.ts_f=e" type="datetime-local" placeholder="ts_f" name="ts_f" 
               style="vertical-align: middle; margin: 2px 2px 0 0; padding: 10px; 
                      background-color: #fff; border: 1px solid #ddd;" />
        <label style="margin: 2px 2px 0 0;padding: 10px 20px;">bool_f</label>
        <input :ref="(e)=>dataSelect.bool_f=e" type="checkbox" placeholder="bool_f" name="bool_f" 
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
    <div class="table_container" @scroll="trottling">
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
          <template v-for="(row, index) in dataView">
          <tr :ref="(el)=>dataView[index].tr = el" @click="rowclick(row)">
            <td v-for="(value, key) in row.data">
             {{value}}
            </td>
          </tr>
          </template>
        </tbody>
      </table>
    </div>
    <p>Показано с {{scroll_r.from}} по {{scroll_r.to}} строки.
      [DEBUG (scroll {{scroll_r.last_scroll}} max {{scroll_r.last_scroll_max}})]</p>
    </div>
  </div>
</template>

<style scoped>
dialog {
    border: 2px solid #111111;
    padding: 2em;
    border-radius: 8px;
    background: linear-gradient(0deg, rgba(78, 78, 78, 1) 0%, rgba(209, 209, 209, 1) 100%);
    box-shadow: 12px 18px 16px 8px rgba(34, 60, 80, 0.2);
    margin: auto; 

}
dialog::backdrop {
  background-color: rgba(54, 54, 54, 0.6);
  backdrop-filter: blur(3px); 
}
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
  background: linear-gradient(90deg, rgba(22, 22, 22, 1) 0%, rgba(11, 118, 139, 1) 100%);
}
.container{
  width: 90vw;
  height: 90vh;
  padding: 10px;
  display: flex;
  flex-direction: column;
  background: linear-gradient(0deg, rgba(153, 145, 155, 1) 0%, rgba(209, 209, 209, 1) 100%);
  border: 2px solid #000000ff;
  border-radius: 10px 10px 10px 10px;
  box-shadow: 12px 18px 16px 8px rgba(34, 60, 80, 0.2);
}

.table_container{
  flex: 1;
  margin-top: 5px;
  border: 2px solid #000000ff;
  background: #d3d3d3ff;
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
  background: #7a6565ff;
}
table, th, td {
    padding: 10px;
  border: 1px solid #3f3f3fff;
}
td > span{
  padding: 10px;
}
</style>

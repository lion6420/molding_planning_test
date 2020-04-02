<template>
<b-container fluid>
  <div>
    <ul v-for="(m, index) in machines" :key="index">
      <li>
        <span>{{ m.name }}</span>
        <span>{{ m.tons }}</span>
        <a-switch style="margin-bottom:5px;margin-left: 15px" checkedChildren="開" unCheckedChildren="關" />
        <a-input-number style="margin-left:20px;width:80px" :min="1" :max="24" v-model="m.totalMachineTime"/>
        <a-select v-model="m.color" class="selectColor">
          <a-select-option value="white">白色</a-select-option>
          <a-select-option value="transparent">透明</a-select-option>
          <a-select-option value="others">其他</a-select-option>
        </a-select>
        <el-divider direction="vertical"></el-divider>
        <el-popover
          v-for="(order, o_index) in m.orders" :key="o_index"
          placement="top-start"
          trigger="hover"
          content="这是一段内容,这是一段内容,这是一段内容,这是一段内容。">
          <el-button :style="{width: `${calculateWidth(order)}`}" slot="reference">{{order.PN}}</el-button>
          <el-button :style="{width: `${4/24*scheduleWidth}`}" slot="reference" disabled>換模</el-button>
        </el-popover>
      </li>
    </ul>
  </div>
</b-container>
</template>

<script>
export default {
  data() {
    return {
      scheduleWidth: 700,
      machines: [ 
        {
          name: 'A01',
          tons: '100T',
          totalMachineTime: 24,
          color: 'white',
          orders: [
            {
              PN: '1B417M800-01E',
              time: 12
            },
            {
              PN: '1B417M800-01E',
              time: 12
            }
          ]
        },
        {
          name: 'A02',
          tons: '100T',
          totalMachineTime: 24,
          color: 'others',
          orders: [
            {
              PN: '1A32RGB00-01E',
              time: 10
            },
            {
              PN: '1B41RQ500K01E',
              time: 14
            }
          ]
        }
      ]
    }
  },
  methods: {
    calculateWidth(order) {
      const btnWidth = order.time/24*this.scheduleWidth
      return btnWidth.toString() + 'px'
    }
  }
}
</script>

<style scoped>
  li {
    font-size: 20px;
    margin-left: 50px;
    margin-top: 40px;
  }
  span {
    margin-left: 15px;
  }
  .selectColor {
    margin-left: 20px;
    margin-right: 50px;
  }
</style>
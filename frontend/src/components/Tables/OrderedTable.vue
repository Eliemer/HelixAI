<template>
  <div>
    <md-table v-model="users" :table-header-color="tableHeaderColor">
      <md-table-row slot="md-table-row" slot-scope="{ item }">
        <md-table-cell md-label="ID">{{ item.id }}</md-table-cell>
        <md-table-cell md-label="Name">{{ item.name }}</md-table-cell>
        <md-table-cell md-label="Class 1">{{ item.class1 }}</md-table-cell>
        <md-table-cell md-label="Class 2">{{ item.class2 }}</md-table-cell>
        <md-table-cell md-label="Total">{{ item.total }}</md-table-cell>
      </md-table-row>
    </md-table>
  </div>
</template>

<script>
export default {
  name: "ordered-table",
  props: {
    tableHeaderColor: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      selected: [],
      users: [
        {
          id: 1,
          name: "HRAS KRAS",
          class1: "77",
          class2: "156",
          total: "233"
        },
        {
          id: 1,
          name: "Kinases",
          class1: "1,773",
          class2: "1,593",
          total: "3,365"
        },
        {
          id: 1,
          name: "TSG/OG",
          class1: "1,176",
          class2: "1,138",
          total: "2,314"
        }
      ]
    };
  }
};
</script>

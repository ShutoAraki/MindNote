<script>
import moment from 'moment';

import { Scatter } from 'vue-chartjs';

export default {
  extends: Scatter,
  props: {
    note_data: Array
  },
  data() {
    return {
      coordinates: [],
      options: {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          display: false
        },
        scales: {
          xAxes: [
            {
              gridLines: {
                display: false,
                drawBorder: false
              },
              ticks: {
                display: false
              }
            }
          ],
          yAxes: [
            {
              gridLines: {
                display: false,
                drawBorder: false
              },
              ticks: {
                display: false
              }
            }
          ]
        },
        tooltips: {
          titleFontSize: 18,
          callbacks: {
            title: (tooltipItem) => {
              return this.note_data[tooltipItem[0]['index']].title;
            },
            label() {
              return ''
            },
            afterLabel: (tooltipItem) => {
              return this.note_data[tooltipItem['index']].content + '\n' + moment(this.note_data[tooltipItem['index']].last_edit).format('M/D/YY HH:mm');
            }
          }
        },
        onClick: (event) => {
          this.handle_click(event);
        }
      }
    };
  },
  async mounted() {
    let shapes = [];
    let radius = [];
    let borderWidth = [];
    let hoverBorderWidth = [];
    for (let i = 0; i < this.note_data.length; i++) {
      this.coordinates.push({ x: this.note_data[i].x, y: this.note_data[i].y });
      shapes.push(this.note_data[i].favorite ? 'star' : 'circle');
      radius.push(this.note_data[i].favorite ? 12 : 8);
      borderWidth.push(this.note_data[i].favorite ? 8 : 0);
      hoverBorderWidth.push(this.note_data[i].favorite ? 5 : 0);
    }
    let note_icon = new Image();
    note_icon.src = 'http://simpleicon.com/wp-content/uploads/note.png';
    note_icon.width = 50;
    note_icon.height = 50;
    this.renderChart(
      {
        datasets: [
          {
            data: this.coordinates,
            backgroundColor: '#ff0000',
            pointRadius: radius,
            pointHoverRadius: 10,
            pointHitRadius: 10,
            pointBorderWidth: 5,
            //pointStyle: note_icon
            pointStyle: shapes,
            pointBackgroundColor: this.note_data.map((note) => note.color),
            pointBorderColor: this.note_data.map((note) => note.color),
            pointHoverBorderWidth: hoverBorderWidth,
          }
        ]
      },
      this.options
    );
  },
  methods: {
    handle_click(event) {
      let elements = this.$data._chart.getElementsAtEvent(event);
      if (elements.length > 0) {
        this.$router.push(`/notes/${this.note_data[elements[0]._index].id}`)
      }
    }
  }
};
</script>

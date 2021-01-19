
// 指定图表的配置项和数据
var result_fig_option = {
    title: {
        text: '收益率对比图',
        textStyle: {
            fontSize: 14,
        },
        left: 'left',
    },
    animation:false,
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'line',
            lineStyle: {
                color: '#7171C6'
            }
        }
    },
    legend: {
        data: ['策略收益率', '期货收益率'],
        left: 'right',
    },
    grid: {
        left: '4%',
        right: '10%',
        bottom: '4%',
        top: 50,
        containLabel: true
    },
    xAxis: [{
        type: 'category',
        data: []
    }],
    yAxis: [{
        type: 'value',
        axisLabel: {
            show: true,
            // color: 'white',
            fontSize: 12,
        },
        axisLine: {
            show: true
        },
        splitLine: {
          show: false//不显示横向分割线
        }
    }],
    series: [{
        name: '策略收益率',
        type: 'line',
        smooth: true,
        data: [],
        markPoint: {
            data: [{
                     name: '最终收益率',
                     coord: [],
                     symbolRotate: -90,
                     value: ''
                }]
        },
        lineStyle: {
            shadowBlur: 2,
            shadowOffsetY: 1
        },
    },{
        name: '期货收益率',
        type: 'line',
        smooth: true,
        data: [],
        markPoint: {
            data: [{
                     name: '最终收益率',
                     coord: [],
                     symbolRotate: -90,
                     value: ''
                }]
        },
    }]
};

var result_fig = echarts.init(document.getElementById('result_fig'));
result_fig.setOption(result_fig_option);
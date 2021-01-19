var all_data=[]

function get_lookback_data() {
    $.ajax({
        type:'GET',
        url: "/result_data",
        contentType:'application/json',
        dataType:'json',

        success: function (data) {
            all_data=data
            document.getElementById('range').setAttribute('max',data.s1.length)
            update_fig()
        },
        error: function () {
            console.log("失败了")
        }
    })
}

function update_fig(){
    let start_day=$("#range").val()
    console.log(start_day)
    result_fig_option.xAxis[0].data = all_data.x_lable.slice(start_day,);
    let small_s1=[]
    let small_s2=[]
    if (!all_data){
        console.log('数据未加载')
        return 0
    }
    for (i=start_day;i<all_data.s1.length;i++){
        small_s1.push((all_data.s1[i]/all_data.s1[start_day]).toFixed(4))
        small_s2.push((all_data.s2[i]/all_data.s2[start_day]).toFixed(4))
    }
    result_fig_option.series[0].data = small_s1;
    result_fig_option.series[1].data = small_s2;

    last_s1=parseFloat(small_s1[small_s1.length-1])
    last_s2=parseFloat(small_s2[small_s2.length-1])
    result_fig_option.series[0].markPoint.data[0].coord=[small_s1.length-1,last_s1]
    result_fig_option.series[0].markPoint.data[0].value='策略收益率\n'+((last_s1-1)*100).toFixed(2)+'%'
    result_fig_option.series[1].markPoint.data[0].coord=[small_s2.length-1,last_s2]
    result_fig_option.series[1].markPoint.data[0].value='期货收益率\n'+((last_s2-1)*100).toFixed(2)+'%'

    result_fig.setOption(result_fig_option);
    // $("#info").text='加载完成'
}


get_lookback_data()
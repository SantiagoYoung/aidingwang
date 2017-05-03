//基础url
// window.baseUrl = "http://123.206.49.101:8018/"
window.baseUrl = "0.0.0.0:8000/"
  // 点击提交留言

$(function() {
  //获取具体类型的留言
  // $(".Website-cons").click(function () {
  //     //获取当前点击的<a>
  //     $.ajax({
  //         type: 'get',
  //         url: window.baseUrl + 'Accounts/get_default_message/',
  //         data: {
  //             type_id: $(this).attr("value")
  //
  //         },
  //         dataType: 'json',
  //         success: function (data) {
  //
  //             var div = []
  //             $('#show_message').text('')
  //             for (var i = 0; i < data.length; i++) {
  //                 div[i] = $("<div>")
  //                 div[i].attr("class", "website-cons-leaving")
  //                 var div1 = $("<div>")
  //                 var label = $("<label>")
  //                 label.text("用户名:")
  //                 div1.append(label)
  //                 var span = $("<span>")
  //                 span.attr("id", "leaving-username")
  //                 span.text(data[i].username)
  //                 div1.append(span)
  //                 var div2 = $("<div>")
  //                 div2.attr("id", "user-leaving")
  //                 div2.text(data[i].content)
  //                 var div3 = $("<div>")
  //                 div3.attr("id", "zzz-time")
  //                 div3.text(data[i].create_time)
  //                 var div4 = $("<div>")
  //                 div4.attr("id", "hf-content")
  //                 div4.text(data[i].com)
  //                 var div5 = $("<div>")
  //                 div5.attr("id", "hf-time")
  //                 div5.text(data[i].comment_time)
  //                 var div6 = $("<div>")
  //                 div6.attr("id", "page_number")
  //                 div6.text(data[i].total_page)
  //                 var div7 = $("<span>")
  //                 div7.text("回复：")
  //                 div1.append(div3)
  //                 div1.append(div2)
  //                 div1.append(div7)
  //                 div1.append(div5)
  //                 div1.append(div4)
  //                 div1.append(div6)
  //                 div[i].append(div1)
  //
  //                 $('#show_message').append(div[i])
  //             }
  //         }
  //     });
  // });


  $('#btn').click(function() {
    //点击事件内进行判断，是否都填入值
    if (!($("#linkman").val() && $("#leaving-content").val())) {
      return
    }
    $.ajax({
      type: "get",
      url: window.baseUrl + 'Accounts/message_board/',
      data: {
        contact: $("#linkman").val(),
        content: $("#leaving-content").val(),
        type_id: $('#m_type').val()
      },
      dataType: 'json',
      success: function(data) {
        if (data.status = 3) {
          alert("发表成功");
          window.location.reload();
        }

      }
    });
  });
  //获取留言并展示 默认战士网站建设
  $.ajax({
    type: "get",
    url: window.baseUrl + 'Accounts/get_default_message/',
    dataType: 'json',
    success: function(data) {
      console.log(data);
      var div = []
      for (var i = 0; i < data.length; i++) {
        div[i] = $("<div>")
        div[i].attr("class", "website-cons-leaving")
        var div1 = $("<div>")
        var label = $("<label>")
        label.attr("class", "label label-info")
        label.text("用户名:")
        div1.append(label)
        var span = $("<span>")
        span.attr("id", "leaving-username")
        span.attr("class", "btn btn-default")
        span.text(data[i].username)
        div1.append(span)
        var div2 = $("<div>")
        div2.attr("id", "user-leaving")
        div2.text(data[i].content)
        var div3 = $("<div>")
        div3.attr("id", "create_time")
        div3.text(data[i].create_time)
        var div4 = $("<div>")
        div4.attr("id", "hf-content")
        div4.text(data[i].com)
        var div5 = $("<div>")
        div5.attr("id", "hf-time")
        div5.text(data[i].comment_time)
        var div6 = $("<div>")
        div6.attr("id", "page_number")
        var div7 = $("<span>")
        div7.attr("class", "hf-title  label label-info")
        div7.text("回复：")
        div1.append(div3)
        div1.append(div2)
        div1.append(div7)
        div1.append(div5)
        div1.append(div4)
        div1.append(div6)
        div[i].append(div1)
        $('#show_message').append(div[i])
      }
    }
  });
  var curpage = 1;
  var tolpage = $("#page_number").text(); //总页数
  var turnpage = $("#next_page_num").text;
  $("#next-page").click(function() {
    curpage = curpage + 1;
    window.curpage = curpage;
    console.log(curpage);
    $("#next_page_num").text(curpage);
    if (curpage != 1) {
      $(".website-cons-leaving").remove();
    }
    $.ajax({
      type: 'get',
      url: '/Accounts/get_default_message/',
      data: {
        page: curpage
      },
      dataType: 'json',
      success: function(data) {
        tolpage = data[0].total_page;
        if (curpage>tolpage) {
          curpage = tolpage;
          return;
        }
        $("#show_message").text("");
        var pag = []
        for (var i = 0; i < data.length; i++) {
          pag[i] = $("<div>")
          pag[i].attr("class", "next_page_con");
          var div_one = $("<div>")
          var lab = $("<label>")
          lab.attr("class", "label label-info")
          lab.text("用户名：")
          div_one.append(lab)
          var spn = $("<span>")
          spn.attr("id", "leaving-username")
          spn.attr("class", "btn btn-default")
          spn.text(data[i].username)
          var div_one_1 = $("<div>")
          div_one_1.attr("id", "user-leaving");
          div_one_1.text(data[i].content)
          div_one.append(spn)
          div_one.append(div_one_1)
          pag[i].append(div_one)
          $("#show_message").append(pag[i]);
        }
      }
    });
  });
  $("#previous-page").click(function() {
    curpage = curpage - 1;
    if (curpage == 0) {
      curpage = 1;
    }
    window.curpage = curpage;
    console.log(curpage);
    $.ajax({
      type: 'get',
      url: '/Accounts/get_default_message/',
      data: {
        page: curpage
      },
      dataType: 'json',
      success: function(data) {
        $("#show_message").text("");
        var pag = []
        for (var i = 0; i < data.length; i++) {
          pag[i] = $("<div>")
          pag[i].attr("class", "next_page_con");
          var div_one = $("<div>")
          var lab = $("<label>")
          lab.attr("class", "label label-info")
          lab.text("用户名：")
          div_one.append(lab)
          var spn = $("<span>")
          spn.attr("id", "leaving-username")
          spn.attr("class", "btn btn-default")
          spn.text(data[i].username)
          var div_one_1 = $("<div>")
          div_one_1.attr("id", "user-leaving");
          div_one_1.text(data[i].content)
          div_one.append(spn)
          div_one.append(div_one_1)
          pag[i].append(div_one)
          $("#show_message").append(pag[i]);
        }
        // if (window.curpage == 0) {
        //   $("#previous-page").attr("disabled", "disabled");
        //   $("#previous-page").css("cursor", "not-allowed");
        // }
      }
    });
  });

  console.log(curpage);
});

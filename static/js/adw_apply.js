/*
 luopeng 2016.11.03
 wab page code integration
 */
$(document).ready(function () {

    //头部未登录提示
    $("#user-collection").mouseover(function () {
        $("#guide-usercollection").show();
    });
    $("#user-collection").mouseout(function () {
        $("#guide-usercollection").hide();
    });

    $("#no-login").click(function () {
        if ($(this).val() == 0) {
            alert("只要登录才能进入此页面哦！");
            window.location.reload();
        }
    });

    $("#joined").click(function () {
        alert("您已入驻过店铺，无法进入！");
    });

    $("#no_login_store").click(function () {
        alert("登录后才能入驻店铺哦！");
    });

    $("#no_login_goods").click(function () {
        alert("登录后才能查看收藏哦！");
    });

    $("#no_login_goods2").click(function () {
        alert("登录后才能查看收藏哦！");
    });

    $("#on_login_sc").click(function () {
        alert("登录后才能进入收藏哦！");
    });

    $("#shops-search").click(function () {
        $("#search_box").attr("name", "store_name");
    });
    $("#commodity-search").click(function () {
        $("#search_box").attr("name", "goods_search");
    });

     //禁止回车键提交表单
    $("form").keypress(function (e) {
        if (e.keyCode == 13) {
            e.preventDefault();
        }
    });

    //首页轮播图
    $(".home-right-imgs").find("#gzdzzs-img").eq(2).attr("id", "gzdzzs-img-over");


    //首页轮播图删除class
    $(".carousel-inner").find(".item").eq(1).removeClass("active");

    //左侧边栏状态提示
    $("#audit_in").click(function () {
        alert("您的店铺正在审核中，请稍等！");
    });

    $("#store_there").click(function () {
        alert("您已入驻过店铺，无法进入！");
    });

    $("#no-store").click(function () {
        alert("您还没有入驻店铺！");
    });

    $("#no-store-up").click(function () {
        alert("您还没有店铺不能上传商品，如需上传商品请入驻店铺！");
    });

    //商品搜索
    $(".img-info-box").mouseover(function () {
        $(this).css("border", "1px solid #ff5250");
    });
    $(".img-info-box").mouseout(function () {
        $(this).css("border", "1px solid #ededed");
    });

    //商品搜索交互
    $("#turn_pag").click(function () {
        var pagenum = $("#turn_page").text();
        $.ajax({

            url: "/catalog/search/",
            type: "get",
            data: {
                page: pagenum

            },
            success: function (data) {
                alert("成功");
            },
            error: function (data) {
                alert("失败");
            }
        });
    });
    $("#turn_page2").click(function () {
        var pagenum = $("#turn_page2").text();
        $.ajax({

            url: "/catalog/search/",
            type: "post",
            data: {
                page: pagenum,
                search_content: $('#search_box').val()
            },
            success: function (data) {
                alert("成功");
            },
            error: function (data) {
                alert("失败");
            }
        });
    });
    //收藏的店铺页面交互
    $("#CheckAll-store").click(function () {
        if (this.checked) {
            $("#mycheckbox :checkbox").prop("checked", true);
        } else {
            $("#mycheckbox :checkbox").prop("checked", false);
        }
    });
    $("#delete-singlestos").click(function () {
        var stores_delete = []
        $("input:checkbox[name='id']:checked").each(function () {
            stores_delete.push($(this).val());
        });
        if (stores_delete.length) {
            $.ajax({
                type: "post",
                url: " /Accounts/delete_collection_store/",
                data: {
                    id: stores_delete
                },
                success: function (data) {
                    alert("删除成功");
                    window.location.reload();
                },
                error: function (data) {
                    alert("删除失败");
                }
            });
        }
    });

    //收藏的商品页面交互
    //全选
    $("#CheckAll-goods").click(function () {
        if (this.checked) {
            $("#mycheckbox :checkbox").prop("checked", true);
        } else {
            $("#mycheckbox :checkbox").prop("checked", false);
        }
    });

    $("#delete-csysinfo").click(function () {
        var goods_delete = []
        $("input:checkbox[name='id']:checked").each(function () {
            goods_delete.push($(this).val());
        });
        if (goods_delete.length) {
            $.ajax({
                type: "post",
                url: " /catalog/delete_collections_goods/",
                data: {
                    id_lists: goods_delete
                },
                success: function (data) {
                    alert("删除成功");
                    window.location.reload();
                },
                error: function (data) {
                    alert("删除失败");
                }
            });
        }
    });

    //上传商品选择分类
    $.getJSON('/catalog/show_type', function (data) {
        console.log(data.data)
//            var data = [{"tab": "job1", "jobS": ["job11", "job12"]}, {"tab": "job2", "jobS": ["job21", "job22"]}]
        for (key in data['data']) {
            $("#province").append(' <option value="' + data['data'][key]['big'] + '">' + data['data'][key]['big'] + '</option>');
        }
        for (key in data['data']) {
            if (data['data'][key]['big'] == $("#province").val()) {
                var len = data['data'][key]['small'].length;
                for (i = 0; i < len; i++) {
                    $("#show-sele").append(' <option value="' + data['data'][key]['id'][i] + '">' + data['data'][key]['small'][i] + '</option>');
                }
            }
        }

        $("#province").change(function () {
            $("#show-sele").children().remove();
            for (key in data['data']) {

                if ($(this).val() == data['data'][key]['big']) {

                    var len = data['data'][key]['small'].length;

                    for (i = 0; i < len; i++) {


                        $("#show-sele").append(' <option value="' + data['data'][key]['id'][i] + '">' + data['data'][key]['small'][i] + '</option>');
                    }
                }
            }
        });
    });

    //商品编辑交互
    $("#click_all").click(function () {
        if (this.checked) {
            $(".upload_is_imgbox :checkbox").prop("checked", true);
        } else {
            $(".upload_is_imgbox :checkbox").prop("checked", false);
        }
    });

    $("#delete-uploimg").click(function () {
        var goods_edit = []
        $("input:checkbox[name='id']:checked").each(function () {
           goods_edit.push($(this).val());
        });
        $.ajax({
            type: "post",
            url: " /catalog/delete_uploaded_picture/",
            data: {
                id: goods_edit
            },
            success: function (data) {
                alert("删除成功");
                window.location.reload();
            },
            error: function (data) {
                alert("失败");
            }
        });
    });
    $("#delete_color").click(function () {
        var colid = window.location.href.split("/")[5];
        console.log(colid);
        $.ajax({
            type: 'post',
            url: '/Accounts/delete_color/',
            data: {
                id: colid
            },
            success: function (data) {
                alert("删除颜色成功！");
                window.location.reload();
            },
            error: function (data) {
                alert("失败");
            }
        });
    });

    //商品小类交互
    $(".turpage_num").click(function () {
        var num = $(".number_1").text();
        alert(num);
        $.ajax({
            type: 'get',
            ulr: '/catalog/ShowGoodsBySmallType/',
            data: {
                page: num
            },
            success: function (data) {
                alert("成功");
                window.location.reload();
            }
        });
    });

    //商品详情页交互
        //收藏商品
        var goodsId = window.location.href.split("/")[5];
        $("#goods_collection").click(function () {
            if ($(this).text().trim() == "收藏商品") {
                $(this).attr("value", "1");
            }
            if ($(this).text().trim() == "取消收藏") {
                $(this).attr("value", "0");
            }
            $.ajax({
                type: "POST",
                url: "/catalog/collections/" + goodsId,
                data: {
                    status: $("#goods_collection").val()
                },
                success: function (data) {
                    window.location.reload();
                },
            });
        });
        //收藏店铺
        var storeId = window.location.href.split("/")[5];
        $("#shops-collection").click(function () {
            if ($(this).text().trim() == "收藏店铺") {
                $(this).attr("value", "1");
            }
            if ($(this).text().trim() == "取消收藏") {
                $(this).attr("value", "0");
            }
            $.ajax({
                type: "post",
                url: "/Store/store_collection/" + storeId,
                data: {
                    status: $("#shops-collection").val()
                },
                success: function (data) {
                    window.location.reload();
                },
            });
        });
    //左侧商品图片预览
    $("#goods_preview li").mouseover(function () {
        $(this).addClass("ad-selected");
    });
    $("#goods_preview li").mouseout(function () {
        $(this).removeClass("ad-selected");
    });
    $("#goods_preview img").each(function () {
        var imgsrc = $(this).attr("src");
        $(this).mouseover(function () {
            $(".ware-left img").attr("src", imgsrc);
        });
        $(this).mouseout(function () {
            $(".ware-left img").attr("src", imgsrc);
        });
    });
});

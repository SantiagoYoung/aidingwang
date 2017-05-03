/**
 * Created by Administrator on 2016/10/8 0008.
 */
		 //搜索选择
       $(function () {
			$("#shops-search").click(function(){
				$(this).addClass("shops-search-hover");
				 if ($("#commodity-search").hasClass("commodity-search-hover")) {
					 $("#commodity-search").removeClass("commodity-search-hover");
				 }

				$('#search_box').attr('name', 'shop_search');

			});
			 $("#commodity-search").click(function(){
				 $(this).addClass("commodity-search-hover");
				 if ($("#shops-search").hasClass("shops-search-hover")) {
					 $("#shops-search").removeClass("shops-search-hover");
				 }
				 $('#search_box').attr('name', 'goods_search');
			 });

			 
       });
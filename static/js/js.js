jQuery(function($){

	$('#vote_up').click(function(){
		value = 1;
		$.ajax({
			url: location.href + 'vote/' + value,
			data: {},
			dataType: 'json',
			success: function(data, textStatus, jqXHR) {
				if (data.success == true) {
					vote = document.getElementById('vote_score').innerHTML;
					document.getElementById('vote_score').innerHTML = parseInt(vote,10) + 1;
				}
				alert(data.message);
			}
		});
	});

	$('#vote_down').click(function(){
		value = 0;

		$.ajax({
			url: location.href + 'vote/' + value,
			data: {},
			dataType: 'json',
			success: function(data, textStatus, jqXHR) {
				if (data.success == true) {
					vote = document.getElementById('vote_score').innerHTML;
					document.getElementById('vote_score').innerHTML = parseInt(vote,10) - 1;
				}
				alert(data.message);
			}
		});
	});

	$('#favourite').click(function(){
		$.ajax({
			url: location.href + 'favourite/',
			data: {},
			dataType: 'json',
			success: function(data, textStatus, jqXHR){
				if (data.success == true) {
					$("#favourite").attr("class","fas fa-star vote_and_fav");
					alert(data.message);
				} else {
					$("#favourite").attr("class","far fa-star vote_and_fav");
					alert(data.message);
					
				}
			}
		});
	});

	$('i[name = "vote_up_to_answer"]').click(function(){
		value = 1;
		answer = $(this).attr('id');
		// alert(answer);
		$.ajax({
			url: location.href + 'vote_to_answer/' + answer + value,
			data: {},
			dataType: 'json',
			success: function(data, textStatus, jqXHR) {
				if (data.success == true) {
					vote = $('strong[name = "' + answer + '"]').text();
					$('strong[name = "' + answer + '"]').text(parseInt(vote,10) + 1);
				}
				alert(data.message);
			}
		});

	});

	$('i[name = "vote_down_to_answer"]').click(function(){
		value = 0;
		answer = $(this).attr('id');
		$.ajax({
			url: location.href + 'vote_to_answer/' + answer + value,
			data: {},
			dataType: 'json',
			success: function(data, textStatus, jqXHR) {
				if (data.success == true) {
					vote = $('strong[name = "' + answer + '"]').text();
					$('strong[name = "' + answer + '"]').text(parseInt(vote,10) - 1);
				}
				alert(data.message);
			}
		});
	});
	$('#notify_button').click(function(){
		$.ajax({
			url: '/inbox/notifications/api/unread_list/?mark_as_read=true',
			data: {},
			dataType: 'json',
			success: function(data,textStatus, jqXHR) {
				// alert('ok');
			}
		});
	});

	$('#img_upload').click(function(){
		file = $("#id_image");
		file.click();
		file.change(function(){
			name =  file.val().split("\\").pop();
			$("#img_upload").text((name.length > 15)?name.slice(0,15) + '...':name.slice(0,10));
		});
	});

	$('#accounts_menu').click(function(){
		if($('#accounts_menu_list').attr('hidden')) {
			$('#accounts_menu_list').attr('hidden', false);
		} 
		else {
			$('#accounts_menu_list').attr('hidden', true);
		}
	});
	// $('pre').attr("class","prettyprint");
});
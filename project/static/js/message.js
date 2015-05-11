function delete_mes(id){
				$('#messageid').val(id);
				$('#myModal').modal('show');
			}
			function do_delete(){
				$('#prousermess_form').submit();
			}
			
			function empty_mes(){
				$('#empty').modal('show');
			}
			function do_empty(){
				$('#empty_form').submit();
			}
			function confirm_mes(id){
				$('#conmessageid').val(id);
				$('#conf_form').submit();
			}
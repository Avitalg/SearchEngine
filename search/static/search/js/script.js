if(window.$){
    $(document).ready(function(){

        var defUrl = 'http://shakespeare.mit.edu/Poetry/sonnets.html';

        if(!!window.words){
            $("#inputText").mark(words,
            {"accuracy":"partially",
            "limiters": [",", "."]});
        }

        $('#go-back').click(function(){
            parent.history.back();
            return false;
        });

        $(".advance_meth").unbind().on("click", function(){
            $("#find").val($("#find").val() + $(this).val());
        });

        $(".default-url-checkbox").on("click", function(){
            if($(this).is(":checked")){
                $('.default-url').val(defUrl);
            } else {
                $('.default-url').val("");
            }
        });


    });
}

 function printFile(URL){
        var myWindow=window.open('','','fullscreen=yes');
        myWindow.document.write("<iframe src="+URL+" width=\"100%\" height=\"100%\"></iframe>");
        myWindow.document.close();
        myWindow.focus();
        $(myWindow.window).load(function(){
            myWindow.print();
        });
 }
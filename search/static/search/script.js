if(window.$){
    $(document).ready(function(){
        if(!!window.words){
            $("#inputText").mark(words,
            {"accuracy":"exactly",
            "limiters": [",", "."]});
        }

        $('#go-back').click(function(){
            parent.history.back();
            return false;
        });

    });
}

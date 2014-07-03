(function() {
    var app = angular.module("admin", ["user", "unit"]);

    app.directive("mainApp", function()
    {
        return {
            restrict : "E",
            templateUrl : "/static/html/mainapp.html",
            controller : function()
            {
                this.selected = 1;

                this.isSelected = function(value){
                    return value == this.selected;
                };

                this.setSelected = function(value){
                    this.selected = value;
                };
            
            },
            controllerAs:"appCtrl",
        };
    });

})();

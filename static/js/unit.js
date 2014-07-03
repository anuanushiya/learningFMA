(function() 
{
    var app = angular.module("unit", []);
    
    app.directive("unitsPanel", function()
    {
        return {
            restrict : "E",
            templateUrl : "/static/html/unitspanel.html",
            controller : function()
            {
            },
            controllerAs: "unitsCtrl",
        };
    });
})();

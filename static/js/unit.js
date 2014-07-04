(function() 
{
    var app = angular.module("unit", []);
    
    app.directive("unitsPanel", function()
    {
        return {
            restrict : "E",
            templateUrl : "/static/html/unitspanel.html",
            controller : [ "$http", function($http)
            {
                var controller = this;
                this.searchField = {};
                this.unitslist = [];
                $http.get("/unitslist").success(function(data)
                    {
                        controller.unitslist = data["units"];
                    });

                this.setSelectedUnit = function(unit)
                {
                    this.selectedUnit = unit;        
                };
                
                this.search = function(){
                };
            }],
            controllerAs: "unitsCtrl",
        };
    });
})();

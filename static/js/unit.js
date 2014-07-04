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
                this.mode = "edit";
                this.searchField = {};
                this.postField = {};
                this.selectedUnit = {};
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

                this.save = function(){
                    if(this.mode == "edit")
                    {
                        $http.put("/updateunit", this.selectedUnit).success(function(data)
                            {
                                alert("Unit updated");
                            });
                    }
                };
            }],
            controllerAs: "unitsCtrl",
        };
    });
})();

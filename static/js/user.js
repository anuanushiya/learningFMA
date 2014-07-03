(function() 
{
    var app = angular.module("user", []);

    app.directive("usersPanel", function()
    {
        return {
            restrict : "E",
            templateUrl : "/static/html/userspanel.html",
            controller : [ "$http", function($http, $scope)
            {
                var controller = this;
                this.searchField = {};
                this.userslist = [];
                $http.get("/userslist").success(function(data)
                    {
                        controller.userslist = data["users"];
                    });

                this.setSelectedUser = function(email)
                {
                    this.selectedUser = {};
                    for(var i = 0; i < this.userslist.length; i++)
                    {
                        if(this.userslist[i].email == email)
                        {
                            this.selectedUser = this.userslist[i];
                            break;
                        }
                    }
                };

                this.search = function(){
                    $http.get("/users?email="+this.searchField.email).success(function(data)
                        {
                            controller.userslist = data["users"];
                        });
                };
            }],
            controllerAs : "usersCtrl",
        };
    });
})();

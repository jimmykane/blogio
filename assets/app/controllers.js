/*
 * @author: Dimitrios Kanellopoulos
 * @contact: jimmykane9@gmail.com
 */

"use strict";

mainApp.controller('index_controller', function($scope, $location) {
    // Nothing for now. Maybe some static stuff
    $scope.go_to_list = function(){
        $location.path('/categories/');
    }
});

mainApp.controller('notifications_controller', function($scope, $timeout, notifications_service) {

    $scope.notifications = [];
    $scope.timeouts = {
        'info': 5000 + 400, //5000 in css
        'warning': 6200 + 400, //6200 in css
        'error': 9400 + 400 //9400 in css
    };

    $scope.$on('handleNotification', function() {

        var notification = {
            'message': notifications_service.message,
            'type': notifications_service.type
        };
        // Here switch on type
        // and fire call back with timer
        $scope.notifications.push(notification);
        // after displaying a bit find and destroy it from the dom as well please its in repeat
        $timeout(function(){
            var index = $scope.notifications.indexOf(notification);
            $scope.notifications.splice(index, 1);
        },$scope.timeouts[notification.type]);
    });

});

mainApp.controller('user_controller', function($location, $scope, users_service,ui) {

    $scope.user = users_service.user();
    $scope.url = $location.absUrl();

    $scope.get_current_user = function() {
        users_service.get_current_user_async().then(
            function(status) {
                // GUI Here
                if (status.code === 200) {
                    //ui.show_notification_info('[OK] GET/User: Found');
                }else if (status.code === 404) {
                    //ui.show_notification_warning('[W] GET/User: Sorry the user was NOT found');
                    $scope.user = false;
                }else{
                    ui.show_notification_warning('Error Undocumented status code');
                    $scope.user = false;
                }
                return;
            },
            function(status){
                console.log('The server encountered an errror');
                return;
            }
        );
    }
    $scope.get_current_user();
});
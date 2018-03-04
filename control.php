
<?php
        $pi = $_GET["pi"];
        $com = $_GET["com"];
        $rigNum = $_GET["rigNum"];
        $installLocation = "./";

        function sendCommand($installLocation, $com, $rigNum) {
                $command = "/usr/bin/python3 ".$installLocation."RRR.py -c ".$com." -r ".$rigNum;
                echo("Command being executed: ".$command);
                $output = exec($command);
                echo "<pre>$output</pre>";
        }

        if ($pi == "local") {
                sendCommand($installLocation, $com, $rigNum);
        };

        header('Location: ./index.php');
        die();
?>

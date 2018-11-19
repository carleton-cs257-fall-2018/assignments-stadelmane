/**
 * Main.java
 * Eric Stadelman and Charlie Broadbent, 20 Nov 2018
 * The main program for breakout in Javafx. The goal of the program is to
 * illustrate our understanding of the MVC model.
 */

package breakout;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.event.EventHandler;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;
import javafx.stage.WindowEvent;

public class Main extends Application {
    @Override
    public void start(Stage primaryStage) throws Exception{
        primaryStage.setResizable(false);
        primaryStage.setOnCloseRequest(new EventHandler<WindowEvent>() {
            @Override
            public void handle(WindowEvent t) {
                Platform.exit();
                System.exit(0);
            }
        });

        FXMLLoader loader = new FXMLLoader(getClass().getResource("breakout.fxml"));
        Parent root = (Parent)loader.load();
        Controller controller = loader.getController();

        primaryStage.setTitle("Break Out");
        Scene scene = new Scene(root, 700, 700);
        scene.getStylesheets().add(getClass().getResource("fleftex.css").toExternalForm());
        primaryStage.setScene(scene);
        scene.setOnKeyPressed(controller);
        primaryStage.show();

        root.requestFocus();
    }


    public static void main(String[] args) {
        launch(args);
    }
}

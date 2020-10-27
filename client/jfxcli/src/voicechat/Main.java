package voicechat;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.TargetDataLine;
import java.net.*;
import java.nio.ByteBuffer;
import java.nio.channels.DatagramChannel;
import java.nio.channels.SocketChannel;

public class Main extends Application {

    @Override
    public void start(Stage primaryStage) throws Exception{
        /*Parent root = FXMLLoader.load(getClass().getResource("voicechat.fxml"));
        primaryStage.setTitle("Hello World");
        primaryStage.setScene(new Scene(root, 300, 275));
        primaryStage.show();*/
        System.out.println("Hello World");
        SocketChannel firstChannel = SocketChannel.open(new InetSocketAddress("192.168.178.0", 12345));
        /*String loginCredentials = "";
        ByteBuffer bb= ByteBuffer.allocate(48);
        bb.clear();
        bb.put(loginCredentials.getBytes());
        bb.flip();
        while(bb.hasRemaining()) {
            firstChannel.write(bb);
        }*/
        firstChannel.close();

        AudioFormat format = new AudioFormat(8000.0f, 16, 1, true, true);
        TargetDataLine microphone = AudioSystem.getTargetDataLine(format);

        DatagramSocket secondChannel = new DatagramSocket();
        InetAddress ip = InetAddress.getByName("192.168.178.0");
        byte[] buffer = null;

        while(true) {
            String input = null;
            assert input != null;
            buffer = input.getBytes();
            DatagramPacket message = new DatagramPacket(buffer, buffer.length, ip, 12345);
            secondChannel.send(message);
        }
    }


    public static void main(String[] args) {
        launch(args);
    }
}

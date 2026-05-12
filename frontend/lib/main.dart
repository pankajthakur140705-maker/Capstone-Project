import 'package:flutter/material.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'dart:convert';
import 'package:http/http.dart' as http;

void main() {
  runApp(const BandhuApp());
}

class BandhuApp extends StatelessWidget {
  const BandhuApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: "Bandhu AI",
      theme: ThemeData(primarySwatch: Colors.blue),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  stt.SpeechToText speech = stt.SpeechToText();
  bool isListening = false;

  String text = "Tap mic and speak...";
  bool isLoading = false;

  String chatResponse = "";
  List<dynamic> schemes = [];

  // ⚡ CHANGE THIS BASED ON DEVICE
  final String baseUrl = "http://10.0.2.2:8000";

  void listen() async {
    if (!isListening) {
      bool available = await speech.initialize();

      if (available) {
        setState(() => isListening = true);

        speech.listen(onResult: (val) {
          setState(() {
            text = val.recognizedWords;
          });
        });
      }
    } else {
      setState(() => isListening = false);
      speech.stop();

      callAPI(text);
    }
  }

  Future<void> callAPI(String message) async {
    setState(() {
      isLoading = true;
      chatResponse = "";
      schemes = [];
    });

    try {
      final response = await http.post(
        Uri.parse("$baseUrl/chat"),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({"message": message}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);

        setState(() {
          chatResponse = data["response"] ?? "";

          if (data["type"] == "scheme_recommendation") {
            schemes = data["data"] ?? [];
          }
        });
      } else {
        setState(() {
          chatResponse = "Server error";
        });
      }
    } catch (e) {
      setState(() {
        chatResponse = "Connection error: $e";
      });
    }

    setState(() {
      isLoading = false;
    });
  }

  Widget buildCard(dynamic scheme) {
    return Card(
      elevation: 5,
      margin: const EdgeInsets.symmetric(vertical: 8),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              scheme["name"] ?? "",
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 6),
            Text("Category: ${scheme["category"] ?? ""}"),
            Text("Description: ${scheme["description"] ?? ""}"),
            if (scheme["reason"] != null)
              Text("AI Reason: ${scheme["reason"]}"),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Bandhu AI 🤖"),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Text(text, style: const TextStyle(fontSize: 18)),

            const SizedBox(height: 20),

            ElevatedButton.icon(
              onPressed: listen,
              icon: Icon(isListening ? Icons.stop : Icons.mic),
              label: Text(isListening ? "Stop" : "Speak"),
            ),

            const SizedBox(height: 20),

            if (isLoading) const CircularProgressIndicator(),

            const SizedBox(height: 10),

            if (chatResponse.isNotEmpty)
              Text(
                chatResponse,
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w500,
                ),
              ),

            const SizedBox(height: 10),

            Expanded(
              child: schemes.isEmpty
                  ? const Text("No schemes yet")
                  : ListView.builder(
                      itemCount: schemes.length,
                      itemBuilder: (context, index) {
                        return buildCard(schemes[index]);
                      },
                    ),
            )
          ],
        ),
      ),
    );
  }
}
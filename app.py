import 'package:flutter/material.dart';
import 'package:flutter_tts/flutter_tts.dart'; // குரல் வாழ்த்துக்காக
import 'dart:async';
import 'dart:math';
import 'package:intl/intl.dart';

void main() => runApp(GangBoysApp());

class GangBoysApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData(brightness: Brightness.dark, primaryColor: Colors.black),
      home: LoginPage(),
    );
  }
}

// --- 1. லாகின் பக்கம் (பெயர், போன், பிறந்ததேதி விவரங்களுடன்) ---
class LoginPage extends StatefulWidget {
  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final TextEditingController _name = TextEditingController();
  final TextEditingController _phone = TextEditingController();
  final TextEditingController _dob = TextEditingController(); // DD-MM
  final TextEditingController _pass = TextEditingController();

  void checkLogin() {
    bool isAdmin = (_pass.text == "admintest@123");
    bool isMember = (_pass.text == "membertest@123");

    if (isAdmin || isMember) {
      String today = DateFormat('dd-MM').format(DateTime.now());
      
      // பிறந்தநாள் தானியங்கி சரிபார்ப்பு
      if (_dob.text == today) {
        Navigator.pushReplacement(context, MaterialPageRoute(
          builder: (context) => BirthdayWishPage(userName: _name.text, isAdmin: isAdmin)
        ));
      } else {
        Navigator.pushReplacement(context, MaterialPageRoute(
          builder: (context) => HomePage(isAdmin: isAdmin, userName: _name.text)
        ));
      }
    } else {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("தவறான பாஸ்வேர்டு!")));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        padding: EdgeInsets.all(30),
        child: Column(
          children: [
            SizedBox(height: 50),
            Image.network('https://i.ibb.co/CpjYwp5r/logo.png', height: 100),
            SizedBox(height: 20),
            Text("GANG BOYS 🥷", style: TextStyle(fontSize: 28, color: Colors.amber, fontWeight: FontWeight.bold)),
            SizedBox(height: 30),
            _inputBox(_name, "பெயர்", Icons.person),
            _inputBox(_phone, "தொலைபேசி எண்", Icons.phone),
            _inputBox(_dob, "பிறந்த தேதி (DD-MM)", Icons.cake),
            _inputBox(_pass, "பாஸ்வேர்டு", Icons.lock, obscure: true),
            SizedBox(height: 30),
            ElevatedButton(
              style: ElevatedButton.styleFrom(backgroundColor: Colors.amber, minimumSize: Size(double.infinity, 50)),
              onPressed: checkLogin,
              child: Text("நுழைவு", style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
            )
          ],
        ),
      ),
    );
  }

  Widget _inputBox(TextEditingController ctrl, String hint, IconData icon, {bool obscure = false}) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: TextField(
        controller: ctrl,
        obscureText: obscure,
        decoration: InputDecoration(prefixIcon: Icon(icon, color: Colors.amber), hintText: hint, filled: true, fillColor: Colors.white10, border: OutlineInputBorder()),
      ),
    );
  }
}

// --- 2. தானியங்கி பிறந்தநாள் வாழ்த்து பக்கம் (குரல் + பலூன்) ---
class BirthdayWishPage extends StatefulWidget {
  final String userName;
  final bool isAdmin;
  BirthdayWishPage({required this.userName, required this.isAdmin});

  @override
  _BirthdayWishPageState createState() => _BirthdayWishPageState();
}

class _BirthdayWishPageState extends State<BirthdayWishPage> with TickerProviderStateMixin {
  FlutterTts flutterTts = FlutterTts();
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _playWish();
    _controller = AnimationController(vsync: this, duration: Duration(seconds: 5))..repeat();
    // 10 விநாடிகளுக்குப் பின் முகப்புப் பக்கத்திற்குச் செல்லும்
    Timer(Duration(seconds: 10), () {
      Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => HomePage(isAdmin: widget.isAdmin, userName: widget.userName)));
    });
  }

  void _playWish() async {
    await flutterTts.setLanguage("ta-IN");
    await flutterTts.speak("இனிய பிறந்தநாள் வாழ்த்துக்கள் ${widget.userName}");
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Stack(
        children: [
          ...List.generate(20, (i) => _buildBalloon()),
          Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Image.network('https://i.ibb.co/CpjYwp5r/logo.png', width: 120),
                SizedBox(height: 20),
                Text("இனிய பிறந்தநாள் வாழ்த்துக்கள்!", style: TextStyle(fontSize: 22, color: Colors.amber)),
                Text(widget.userName, style: TextStyle(fontSize: 40, fontWeight: FontWeight.bold)),
                Text("GANG BOYS 🥷", style: TextStyle(color: Colors.white54)),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildBalloon() {
    double left = Random().nextDouble() * 400;
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) => Positioned(
        bottom: _controller.value * 800,
        left: left,
        child: Icon(Icons.circle, color: Colors.primaries[Random().nextInt(Colors.primaries.length)], size: 40),
      ),
    );
  }
}

// --- 3. முகப்புப் பக்கம் (வலது மூலையில் லோகோவுடன்) ---
class HomePage extends StatelessWidget {
  final bool isAdmin;
  final String userName;
  HomePage({required this.isAdmin, required this.userName});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("GANG BOYS"),
        actions: [Padding(padding: EdgeInsets.all(8), child: Image.network('https://i.ibb.co/CpjYwp5r/logo.png'))],
      ),
      body: Column(
        children: [
          Container(
            padding: EdgeInsets.all(15),
            color: Colors.amber,
            width: double.infinity,
            child: Text("அன்புடன் GANG BOYS குழுவிற்கு வரவேற்கிறோம், $userName!", textAlign: TextAlign.center, style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
          ),
          // இங்கே மற்ற வசதிகள் (ID Card, வரவு செலவு) லிஸ்டாக வரும்
        ],
      ),
    );
  }
}

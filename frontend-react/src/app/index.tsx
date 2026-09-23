import React, { useRef, useState } from "react";
const API_URL = "http://127.0.0.1:8000";
import {
  StyleSheet,
  Text,
  View,
  Pressable,
  TextInput,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
} from "react-native";
import { Canvas, useFrame } from "@react-three/fiber";
import {
  OrbitControls,
  Sphere,
  MeshDistortMaterial,
} from "@react-three/drei";
import * as THREE from "three";

/* =========================
   3D BACKGROUND
========================= */

function AIOrb() {
  const meshRef = useRef<THREE.Mesh>(null);

  useFrame((_, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.x += delta * 0.15;
      meshRef.current.rotation.y += delta * 0.3;
    }
  });

  return (
    <Sphere ref={meshRef} args={[1.5, 64, 64]} scale={1.1}>
      <MeshDistortMaterial
        color="#4f46e5"
        emissive="#312e81"
        emissiveIntensity={1}
        roughness={0.15}
        metalness={0.8}
        distort={0.35}
        speed={2}
      />
    </Sphere>
  );
}

function Particles() {
  const particlesRef = useRef<THREE.Points>(null);

  const particleCount = 500;

  const positions = React.useMemo(() => {
    const data = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount * 3; i++) {
      data[i] = (Math.random() - 0.5) * 12;
    }

    return data;
  }, []);

  useFrame((_, delta) => {
    if (particlesRef.current) {
      particlesRef.current.rotation.y += delta * 0.03;
      particlesRef.current.rotation.x += delta * 0.01;
    }
  });

  return (
    <points ref={particlesRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          args={[positions, 3]}
        />
      </bufferGeometry>

      <pointsMaterial
        size={0.025}
        color="#818cf8"
        transparent
        opacity={0.8}
      />
    </points>
  );
}

function Background3D() {
  return (
    <View style={styles.background3D}>
      <Canvas camera={{ position: [0, 0, 5], fov: 45 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[3, 3, 3]} intensity={5} />
        <pointLight position={[-3, -2, 2]} intensity={3} />

        <Particles />
        <AIOrb />

        <OrbitControls
          enableZoom={false}
          enablePan={false}
          autoRotate
          autoRotateSpeed={0.5}
        />
      </Canvas>
    </View>
  );
}

/* =========================
   SIGNUP SCREEN
========================= */

function SignupScreen({
  onBack,
  onLogin,
}: {
  onBack: () => void;
  onLogin: () => void;
}) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const validateEmail = (value: string) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value);
  };

  const validatePassword = (value: string) => {
    return (
      value.length >= 8 &&
      /[A-Z]/.test(value) &&
      /[a-z]/.test(value) &&
      /[0-9]/.test(value) &&
      /[^A-Za-z0-9]/.test(value)
    );
  };

const handleSignup = async () => {
  setError("");
  setSuccess("");

  if (!name.trim()) {
    setError("Please enter your name.");
    return;
  }

  if (!email.trim()) {
    setError("Please enter your email.");
    return;
  }

  if (!password) {
    setError("Please enter your password.");
    return;
  }

  if (password !== confirmPassword) {
    setError("Passwords do not match.");
    return;
  }

  try {
    const response = await fetch(`${API_URL}/signup`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: name.trim(),
        email: email.trim(),
        password: password,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      setError(data.detail || "Signup failed.");
      return;
    }

    setSuccess("Account created successfully! You can now login.");

    setTimeout(() => {
      onLogin();
    }, 1000);
  } catch (error) {
    console.error("Signup error:", error);
    setError(
      "Unable to connect to the backend. Make sure the backend server is running."
    );
  }
};
  return (
    <KeyboardAvoidingView
      style={styles.keyboardContainer}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
    >
      <ScrollView
        contentContainerStyle={styles.signupScroll}
        keyboardShouldPersistTaps="handled"
      >
        <View style={styles.signupCard}>

          <Pressable
            style={styles.backButton}
            onPress={onBack}
          >
            <Text style={styles.backText}>← Back</Text>
          </Pressable>

          <Text style={styles.signupTitle}>
            Create Account
          </Text>

          <Text style={styles.signupSubtitle}>
            Start your intelligent research journey.
          </Text>

          <Text style={styles.label}>
            Name
          </Text>

          <TextInput
            style={styles.input}
            placeholder="Enter your name"
            placeholderTextColor="#64748b"
            value={name}
            onChangeText={setName}
            autoCapitalize="words"
          />

          <Text style={styles.label}>
            Email
          </Text>

          <TextInput
            style={styles.input}
            placeholder="Enter your email"
            placeholderTextColor="#64748b"
            value={email}
            onChangeText={setEmail}
            keyboardType="email-address"
            autoCapitalize="none"
            autoCorrect={false}
          />

          <Text style={styles.label}>
            Password
          </Text>

          <View style={styles.passwordContainer}>
            <TextInput
              style={styles.passwordInput}
              placeholder="Create a password"
              placeholderTextColor="#64748b"
              value={password}
              onChangeText={setPassword}
              secureTextEntry={!showPassword}
              autoCapitalize="none"
            />

            <Pressable
              onPress={() => setShowPassword(!showPassword)}
            >
              <Text style={styles.showButton}>
                {showPassword ? "HIDE" : "SHOW"}
              </Text>
            </Pressable>
          </View>

          <Text style={styles.passwordHint}>
            Minimum 8 characters with uppercase, lowercase,
            number, and special character.
          </Text>

          <Text style={styles.label}>
            Confirm Password
          </Text>

          <View style={styles.passwordContainer}>
            <TextInput
              style={styles.passwordInput}
              placeholder="Confirm your password"
              placeholderTextColor="#64748b"
              value={confirmPassword}
              onChangeText={setConfirmPassword}
              secureTextEntry={!showConfirmPassword}
              autoCapitalize="none"
            />

            <Pressable
              onPress={() =>
                setShowConfirmPassword(!showConfirmPassword)
              }
            >
              <Text style={styles.showButton}>
                {showConfirmPassword ? "HIDE" : "SHOW"}
              </Text>
            </Pressable>
          </View>

          {error ? (
            <Text style={styles.errorText}>
              {error}
            </Text>
          ) : null}

          {success ? (
            <Text style={styles.successText}>
              {success}
            </Text>
          ) : null}

          <Pressable
            style={({ pressed }) => [
              styles.createButton,
              pressed && styles.buttonPressed,
            ]}
            onPress={handleSignup}
          >
            <Text style={styles.createButtonText}>
              CREATE ACCOUNT
            </Text>
          </Pressable>

          <View style={styles.loginRow}>
            <Text style={styles.loginText}>
              Already have an account?{" "}
            </Text>

            <Pressable onPress={onLogin}>
              <Text style={styles.loginLink}>
                Login
              </Text>
            </Pressable>
          </View>

          <Text style={styles.securityText}>
            Your password is securely processed by the backend.
          </Text>

        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

/* =========================
   LOGIN SCREEN
========================= */

function LoginScreen({
  onBack,
  onDashboard,
  onSignup,
}: {
  onBack: () => void;
  onDashboard: () => void;
  onSignup: () => void;
}) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");

  const validateEmail = (value: string) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value);
  };

  const handleLogin = async () => {
    setError("");

    if (!email.trim()) {
      setError("Please enter your email.");
      return;
    }

    if (!validateEmail(email.trim())) {
      setError("Please enter a valid email address.");
      return;
    }

    if (!password) {
      setError("Please enter your password.");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email.trim(),
          password: password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Invalid email or password.");
        return;
      }

      console.log("Login successful:", data);

      onDashboard();
    } catch (error) {
      console.error("Login error:", error);
      setError(
        "Unable to connect to the backend. Make sure the backend server is running."
      );
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.keyboardContainer}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
    >
      <ScrollView
        contentContainerStyle={styles.loginScroll}
        keyboardShouldPersistTaps="handled"
      >
        <View style={styles.loginCard}>
          <Pressable
            style={styles.backButton}
            onPress={onBack}
          >
            <Text style={styles.backText}>← Back</Text>
          </Pressable>

          <Text style={styles.loginTitle}>
            Welcome Back
          </Text>

          <Text style={styles.signupSubtitle}>
            Login to your Auto Research AI account.
          </Text>

          <Text style={styles.label}>
            Email
          </Text>

          <TextInput
            style={styles.input}
            placeholder="Enter your email"
            placeholderTextColor="#64748b"
            value={email}
            onChangeText={setEmail}
            keyboardType="email-address"
            autoCapitalize="none"
            autoCorrect={false}
          />

          <Text style={styles.label}>
            Password
          </Text>

          <View style={styles.passwordContainer}>
            <TextInput
              style={styles.passwordInput}
              placeholder="Enter your password"
              placeholderTextColor="#64748b"
              value={password}
              onChangeText={setPassword}
              secureTextEntry={!showPassword}
              autoCapitalize="none"
            />

            <Pressable
              onPress={() => setShowPassword(!showPassword)}
            >
              <Text style={styles.showButton}>
                {showPassword ? "HIDE" : "SHOW"}
              </Text>
            </Pressable>
          </View>

          {error ? (
            <Text style={styles.errorText}>
              {error}
            </Text>
          ) : null}

          <Pressable
            style={({ pressed }) => [
              styles.createButton,
              pressed && styles.buttonPressed,
            ]}
            onPress={handleLogin}
          >
            <Text style={styles.createButtonText}>
              LOGIN
            </Text>
          </Pressable>

          <View style={styles.loginRow}>
            <Text style={styles.loginText}>
              Don't have an account?{" "}
            </Text>

            <Pressable onPress={onSignup}>
              <Text style={styles.loginLink}>
                Sign Up
              </Text>
            </Pressable>
          </View>

          <Text style={styles.securityText}>
            Your account is securely verified by the backend.
          </Text>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

/* =========================
   RESEARCH DASHBOARD
========================= */

function Dashboard({
  onLogout,
}: {
  onLogout: () => void;
}) {
  const [search, setSearch] = useState("");

  const handleSearch = () => {
    if (!search.trim()) {
      return;
    }

    console.log("Research query:", search);
  };

  return (
    <View style={styles.dashboard}>
      <View style={styles.dashboardHeader}>
        <View>
          <Text style={styles.dashboardLogo}>
            AUTO RESEARCH AI
          </Text>

          <Text style={styles.dashboardWelcome}>
            Your intelligent research workspace
          </Text>
        </View>

        <Pressable
          style={styles.logoutButton}
          onPress={onLogout}
        >
          <Text style={styles.logoutText}>LOGOUT</Text>
        </Pressable>
      </View>

      <View style={styles.dashboardContent}>
        <Text style={styles.dashboardTitle}>
          What do you want to research?
        </Text>

        <Text style={styles.dashboardSubtitle}>
          Enter a topic and let Auto Research AI generate
          intelligent research.
        </Text>

        <View style={styles.searchContainer}>
          <TextInput
            style={styles.searchInput}
            placeholder="Search any research topic..."
            placeholderTextColor="#64748b"
            value={search}
            onChangeText={setSearch}
            onSubmitEditing={handleSearch}
          />

          <Pressable
            style={({ pressed }) => [
              styles.searchButton,
              pressed && styles.buttonPressed,
            ]}
            onPress={handleSearch}
          >
            <Text style={styles.searchButtonText}>
              SEARCH
            </Text>
          </Pressable>
        </View>

        <View style={styles.dashboardCards}>
          <View style={styles.dashboardCard}>
            <Text style={styles.cardIcon}>🔎</Text>
            <Text style={styles.cardTitle}>
              Research Topics
            </Text>
            <Text style={styles.cardDescription}>
              Search and explore any topic.
            </Text>
          </View>

          <View style={styles.dashboardCard}>
            <Text style={styles.cardIcon}>🤖</Text>
            <Text style={styles.cardTitle}>
              AI Analysis
            </Text>
            <Text style={styles.cardDescription}>
              AI-powered analysis will come here.
            </Text>
          </View>

          <View style={styles.dashboardCard}>
            <Text style={styles.cardIcon}>📊</Text>
            <Text style={styles.cardTitle}>
              Research Reports
            </Text>
            <Text style={styles.cardDescription}>
              Your generated reports will appear here.
            </Text>
          </View>
        </View>
      </View>
    </View>
  );
};

/* =========================
   MAIN APP
========================= */

export default function HomeScreen() {
  const [screen, setScreen] = useState<
    "home" | "signup" | "login" | "dashboard"
  >("home");

  if (screen === "signup") {
    return (
      <SignupScreen
        onBack={() => setScreen("home")}
        onLogin={() => setScreen("login")}
      />
    );
  }

  if (screen === "login") {
    return (
      <LoginScreen
        onBack={() => setScreen("home")}
        onDashboard={() => setScreen("dashboard")}
        onSignup={() => setScreen("signup")}
      />
    );
  }

  if (screen === "dashboard") {
    return (
      <Dashboard
        onLogout={() => setScreen("home")}
      />
    );
  }

  return (
    <View style={styles.container}>
      <Background3D />

      <View style={styles.darkOverlay} />

      <View style={styles.content}>
        <Text style={styles.smallTitle}>
          WELCOME TO
        </Text>

        <Text style={styles.title}>
          AUTO
        </Text>

        <Text style={styles.title}>
          RESEARCH AI
        </Text>

        <Text style={styles.subtitle}>
          Intelligent Research.{"\n"}
          Faster Insights. Smarter Decisions.
        </Text>

        <Pressable
          style={({ pressed }) => [
            styles.button,
            pressed && styles.buttonPressed,
          ]}
          onPress={() => setScreen("signup")}
        >
          <Text style={styles.buttonText}>
            CREATE NEW ACCOUNT
          </Text>
        </Pressable>

        <Pressable
          style={styles.existingAccountButton}
          onPress={() => setScreen("login")}
        >
          <Text style={styles.existingAccountText}>
            Already have an account? Login
          </Text>
        </Pressable>
      </View>
    </View>
  );
}

/* =========================
   STYLES
========================= */

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#050816",
    minHeight: "100%",
  },

  background3D: {
    position: "absolute",
    width: "100%",
    height: "100%",
  },

  darkOverlay: {
    position: "absolute",
    width: "100%",
    height: "100%",
    backgroundColor: "rgba(5, 8, 22, 0.55)",
  },

  content: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    paddingHorizontal: 30,
  },

  smallTitle: {
    fontSize: 14,
    letterSpacing: 5,
    color: "#a5b4fc",
    marginBottom: 12,
  },

  title: {
    fontSize: 48,
    fontWeight: "900",
    letterSpacing: 4,
    color: "#ffffff",
    textAlign: "center",
    lineHeight: 54,
  },

  subtitle: {
    marginTop: 22,
    fontSize: 17,
    lineHeight: 27,
    color: "#cbd5e1",
    textAlign: "center",
  },

  button: {
    marginTop: 35,
    paddingVertical: 17,
    paddingHorizontal: 32,
    borderRadius: 14,
    backgroundColor: "#6366f1",
    shadowColor: "#6366f1",
    shadowOffset: {
      width: 0,
      height: 8,
    },
    shadowOpacity: 0.45,
    shadowRadius: 18,
    elevation: 10,
  },

  buttonPressed: {
    transform: [{ scale: 0.96 }],
    opacity: 0.85,
  },

  buttonText: {
    color: "#ffffff",
    fontSize: 14,
    fontWeight: "800",
    letterSpacing: 1.5,
  },

  existingAccountButton: {
    marginTop: 18,
  },

  existingAccountText: {
    color: "#a5b4fc",
    fontSize: 13,
  },

  keyboardContainer: {
    flex: 1,
  },

  signupScroll: {
    flexGrow: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 25,
  },

  signupCard: {
    width: "100%",
    maxWidth: 500,
    backgroundColor: "rgba(15, 23, 42, 0.94)",
    borderRadius: 24,
    padding: 30,
    borderWidth: 1,
    borderColor: "rgba(129, 140, 248, 0.35)",
  },

  backButton: {
    marginBottom: 20,
  },

  backText: {
    color: "#a5b4fc",
    fontSize: 15,
    fontWeight: "600",
  },

  signupTitle: {
    color: "#ffffff",
    fontSize: 32,
    fontWeight: "800",
    marginBottom: 8,
  },

  signupSubtitle: {
    color: "#94a3b8",
    fontSize: 15,
    marginBottom: 28,
  },

  label: {
    color: "#e2e8f0",
    fontSize: 14,
    fontWeight: "600",
    marginBottom: 8,
    marginTop: 14,
  },

  input: {
    height: 52,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: "#334155",
    backgroundColor: "rgba(15, 23, 42, 0.8)",
    color: "#ffffff",
    paddingHorizontal: 16,
    fontSize: 15,
  },

  passwordContainer: {
    height: 52,
    flexDirection: "row",
    alignItems: "center",
    borderRadius: 12,
    borderWidth: 1,
    borderColor: "#334155",
    backgroundColor: "rgba(15, 23, 42, 0.8)",
  },

  passwordInput: {
    flex: 1,
    height: "100%",
    color: "#ffffff",
    paddingHorizontal: 16,
    fontSize: 15,
  },

  showButton: {
    color: "#a5b4fc",
    fontWeight: "700",
    paddingHorizontal: 15,
  },

  passwordHint: {
    color: "#64748b",
    fontSize: 11,
    marginTop: 8,
    lineHeight: 17,
  },

  errorText: {
    color: "#f87171",
    fontSize: 13,
    marginTop: 18,
    lineHeight: 20,
  },

  successText: {
    color: "#4ade80",
    fontSize: 13,
    marginTop: 18,
    lineHeight: 20,
  },

  createButton: {
    marginTop: 24,
    height: 54,
    borderRadius: 13,
    backgroundColor: "#6366f1",
    justifyContent: "center",
    alignItems: "center",
  },

  createButtonText: {
    color: "#ffffff",
    fontSize: 14,
    fontWeight: "800",
    letterSpacing: 1.5,
  },

  loginRow: {
    flexDirection: "row",
    justifyContent: "center",
    marginTop: 22,
  },

  loginText: {
    color: "#64748b",
    fontSize: 13,
  },

  loginLink: {
    color: "#a5b4fc",
    fontSize: 13,
    fontWeight: "700",
  },

  securityText: {
    color: "#64748b",
    textAlign: "center",
    fontSize: 12,
    marginTop: 20,
  },

  loginScroll: {
    flexGrow: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 25,
  },

  loginCard: {
    width: "100%",
    maxWidth: 500,
    backgroundColor: "rgba(15, 23, 42, 0.94)",
    borderRadius: 24,
    padding: 30,
    borderWidth: 1,
    borderColor: "rgba(129, 140, 248, 0.35)",
  },

  loginTitle: {
    color: "#ffffff",
    fontSize: 32,
    fontWeight: "800",
    marginTop: 25,
    marginBottom: 8,
  },

  dashboard: {
    flex: 1,
    backgroundColor: "#050816",
  },

  dashboardHeader: {
    paddingHorizontal: 30,
    paddingTop: 35,
    paddingBottom: 25,
    borderBottomWidth: 1,
    borderBottomColor: "#1e293b",
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },

  dashboardLogo: {
    color: "#ffffff",
    fontSize: 22,
    fontWeight: "900",
    letterSpacing: 2,
  },

  dashboardWelcome: {
    color: "#64748b",
    fontSize: 12,
    marginTop: 5,
  },

  logoutButton: {
    borderWidth: 1,
    borderColor: "#475569",
    borderRadius: 10,
    paddingVertical: 10,
    paddingHorizontal: 16,
  },

  logoutText: {
    color: "#cbd5e1",
    fontSize: 12,
    fontWeight: "700",
  },

  dashboardContent: {
    flex: 1,
    alignItems: "center",
    paddingHorizontal: 25,
    paddingTop: 80,
  },

  dashboardTitle: {
    color: "#ffffff",
    fontSize: 38,
    fontWeight: "900",
    textAlign: "center",
  },

  dashboardSubtitle: {
    color: "#94a3b8",
    fontSize: 15,
    textAlign: "center",
    maxWidth: 600,
    marginTop: 14,
    lineHeight: 23,
  },

  searchContainer: {
    width: "100%",
    maxWidth: 700,
    flexDirection: "row",
    marginTop: 35,
  },

  searchInput: {
    flex: 1,
    height: 58,
    borderWidth: 1,
    borderColor: "#334155",
    backgroundColor: "#0f172a",
    borderRadius: 14,
    color: "#ffffff",
    paddingHorizontal: 20,
    fontSize: 15,
  },

  searchButton: {
    height: 58,
    marginLeft: 10,
    paddingHorizontal: 25,
    borderRadius: 14,
    backgroundColor: "#6366f1",
    justifyContent: "center",
    alignItems: "center",
  },

  searchButtonText: {
    color: "#ffffff",
    fontWeight: "800",
    letterSpacing: 1,
  },

  dashboardCards: {
    width: "100%",
    maxWidth: 900,
    flexDirection: "row",
    justifyContent: "center",
    gap: 15,
    marginTop: 50,
    flexWrap: "wrap",
  },

  dashboardCard: {
    width: 260,
    minHeight: 150,
    padding: 22,
    borderRadius: 18,
    borderWidth: 1,
    borderColor: "#1e293b",
    backgroundColor: "#0f172a",
  },

  cardIcon: {
    fontSize: 25,
    marginBottom: 12,
  },

  cardTitle: {
    color: "#ffffff",
    fontSize: 16,
    fontWeight: "700",
  },

  cardDescription: {
    color: "#64748b",
    fontSize: 13,
    marginTop: 8,
    lineHeight: 19,
  },
});
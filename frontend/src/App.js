import React from "react";
import "./styling/App.scss";

import Header from "./components/Header";
import FileUpload from "./components/FileUpload";

import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <div className="App">
      <Header />
      <div className="container">
        <div className="wrapper">
          <Routes>
            <Route path="/" element={<FileUploadPage />} />
            <Route path="/features" element={<Features />} />
            <Route path="/how-it-works" element={<HowItWorks />} />
            <Route path="/contact-us" element={<Contact />} />
            <Route path="/file-upload" element={<FileUploadPage />} />
          </Routes>
        </div>
      </div>
    </div>
  );
}

function Home() {
  return (
    <div className="container">
      <div className="wrapper">
        <h5>
          Welcome to <b>PodGen</b>, a creative platform to generate podcasts
          from any PDF!
        </h5>
        <p>Click below to try our file upload service:</p>
        <a href="/file-upload" className="btn">
          Upload a PDF
        </a>
      </div>
    </div>
  );
}

function Features() {
  return (
    <div className="container mx-auto py-12">
      <div className="text-center mb-12">
        <h2 className="text-4xl font-extrabold text-gray-900">Discover PodGen's Powerful Features</h2>
        <p className="text-lg text-gray-600 mt-4">Transform your PDFs into engaging podcasts with just a few clicks.</p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {[
          {
            title: 'Transform PDFs',
            description: 'Convert your PDFs into engaging podcasts effortlessly.',
            icon: '📄',
          },
          {
            title: 'Customize Voices',
            description: 'Choose tones, accents, and languages to suit your preferences.',
            icon: '🎙️',
          },
          {
            title: 'Chapter-Based Episodes',
            description: 'Automatically generate chapter-based podcast episodes for better content navigation.',
            icon: '📚',
          },
          {
            title: 'AI-Driven Enhancements',
            description: 'Enhance your podcast with AI-driven summaries, intros, and transitions.',
            icon: '🤖',
          },
          {
            title: 'Seamless Sharing',
            description: 'Easily share your podcasts on all major platforms.',
            icon: '🔗',
          },
        ].map((feature, index) => (
          <div key={index} className="bg-white p-6 rounded-lg shadow-lg">
            <div className="text-4xl text-center">{feature.icon}</div>
            <h3 className="text-xl font-semibold text-center mt-4">{feature.title}</h3>
            <p className="text-gray-600 text-center mt-2">{feature.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

function HowItWorks() {
  return (
    <div className="container mx-auto py-12">
      <div className="text-center mb-12">
        <h2 className="text-4xl font-extrabold text-gray-900">How PodGen Works</h2>
        <p className="text-lg text-gray-600 mt-4">A simple 4-step process to create your podcast.</p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        {[
          {
            step: '1',
            title: 'Upload Your PDF',
            description: 'Upload any PDF file—reports, eBooks, study materials, or scripts.',
            icon: '📤',
          },
          {
            step: '2',
            title: 'AI-Driven Conversion',
            description: 'Our AI processes your document and converts it into a podcast, complete with natural-sounding narration.',
            icon: '🤖',
          },
          {
            step: '3',
            title: 'Customize Your Podcast',
            description: 'Choose narration style, speed, and language to match your target audience.',
            icon: '🎧',
          },
          {
            step: '4',
            title: 'Download and Share',
            description: 'Download your podcast in your preferred format and share it with your network.',
            icon: '📥',
          },
        ].map((step, index) => (
          <div key={index} className="bg-white p-6 rounded-lg shadow-lg">
            <div className="text-4xl text-center">{step.icon}</div>
            <h3 className="text-xl font-semibold text-center mt-4">{step.title}</h3>
            <p className="text-gray-600 text-center mt-2">{step.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}


function Contact() {
  return (
    <div className="container mx-auto py-12">
      <div className="text-center mb-12">
        <h2 className="text-4xl font-extrabold text-gray-900">Contact Us</h2>
        <p className="text-lg text-gray-600 mt-4">Have questions? Feel free to reach out to us via email or our contact form.</p>
      </div>
      <div className="flex justify-center">
        <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-lg">
          <form>
            <div className="mb-4">
              <label htmlFor="name" className="block text-gray-700">Your Name</label>
              <input
                type="text"
                id="name"
                name="name"
                className="w-full p-3 mt-2 border border-gray-300 rounded-lg"
                placeholder="Enter your name"
              />
            </div>
            <div className="mb-4">
              <label htmlFor="email" className="block text-gray-700">Your Email</label>
              <input
                type="email"
                id="email"
                name="email"
                className="w-full p-3 mt-2 border border-gray-300 rounded-lg"
                placeholder="Enter your email"
              />
            </div>
            <div className="mb-4">
              <label htmlFor="message" className="block text-gray-700">Your Message</label>
              <textarea
                id="message"
                name="message"
                className="w-full p-3 mt-2 border border-gray-300 rounded-lg"
                placeholder="Enter your message"
                rows="4"
              ></textarea>
            </div>
            <button
              type="submit"
              className="w-full py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700"
            >
              Send Message
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}


function FileUploadPage() {
  return (
    <div className="container mx-auto p-12">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
        {/* Left Column: Welcome Message */}
        <div className="flex flex-col justify-center items-start space-y-6">
          <h1 className="text-5xl font-bold text-gray-800">
            Welcome to <span className="text-blue-500">PodGen</span>
          </h1>
          <p className="text-xl text-gray-600">
            A creative platform to generate podcasts from any PDF!
          </p>
        </div>

        {/* Right Column: File Upload */}
        <div className="flex justify-center items-center">
          <FileUpload />
        </div>
      </div>
    </div>
  );
  // return (
  //   <>
  //   <div className="container">
  //     <div className="wrapper">
  //       <h5>
  //         Welcome to <b>PodGen</b>, a creative platform to generate podcasts
  //         from any PDF!
  //       </h5>
  //     </div>
  //   </div>
  //     <div className="container">
  //       <div className="wrapper">
  //         <FileUpload />
  //       </div>
  //     </div>
  //   </>
  // );
}

export default App;

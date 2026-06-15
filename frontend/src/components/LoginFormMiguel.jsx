import React, { useState } from 'react';

export default function LoginForm() {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');
    try {
      const response = await fetch('/api/users/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });
      const data = await response.json();
      if (response.ok && data.valido) {
        setMessage('Login successful! Welcome back.');
        // Here you would typically save the token or userId to localStorage/sessionStorage
        localStorage.setItem('userId', data.userId);
        // And then redirect the user
        // window.location.href = '/dashboard';
      } else {
        setMessage(data.message || data.error_message || 'Login failed. Invalid credentials.');
      }
    } catch (error) {
      setMessage('Error connecting to the server.');
    }
    setLoading(false);
  };

  const styles = {
    container: { maxWidth: '400px', margin: '0 auto', backgroundColor: '#1f2937', padding: '30px', borderRadius: '12px', color: 'white', fontFamily: 'sans-serif' },
    formGroup: { marginBottom: '15px' },
    label: { display: 'block', marginBottom: '5px', fontSize: '0.9rem', color: '#9ca3af' },
    input: { width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #374151', backgroundColor: '#374151', color: 'white', boxSizing: 'border-box' },
    button: { width: '100%', padding: '10px', backgroundColor: '#3b82f6', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold', marginTop: '10px' },
    message: { marginTop: '15px', textAlign: 'center', fontSize: '0.9rem', color: '#fbbf24' },
    title: { textAlign: 'center', color: '#3b82f6', marginBottom: '20px' }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Login</h2>
      <form onSubmit={handleSubmit}>
        <div style={styles.formGroup}>
          <label style={styles.label}>Username</label>
          <input type="text" name="username" value={formData.username} onChange={handleChange} required style={styles.input} />
        </div>
        <div style={styles.formGroup}>
          <label style={styles.label}>Password</label>
          <input type="password" name="password" value={formData.password} onChange={handleChange} required style={styles.input} />
        </div>
        <button type="submit" disabled={loading} style={{...styles.button, opacity: loading ? 0.7 : 1}}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      {message && <div style={styles.message}>{message}</div>}
      <div style={{textAlign: 'center', marginTop: '15px', fontSize: '0.9rem'}}>
        <a href="/registerMiguel" style={{color: '#10b981', textDecoration: 'none'}}>Don't have an account? Register here.</a>
      </div>
    </div>
  );
}

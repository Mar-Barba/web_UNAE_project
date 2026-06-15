import React, { useState } from 'react';

export default function RegisterForm() {
  const [formData, setFormData] = useState({
    username: '',
    mail: '',
    password: '',
    rol: 'student', // default role
    group: "1" // default group
  });
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const value = e.target.value;
    setFormData({
      ...formData,
      [e.target.name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');
    try {
      const response = await fetch('/api/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });
      const data = await response.json();
      if (response.ok) {
        setMessage('Registration successful! You can now log in.');
        setFormData({ username: '', mail: '', password: '', rol: 'student', group: "1" });
      } else {
        setMessage(data.message || 'Registration failed.');
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
    select: { width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #374151', backgroundColor: '#374151', color: 'white', boxSizing: 'border-box', appearance: 'none' },
    button: { width: '100%', padding: '10px', backgroundColor: '#10b981', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold', marginTop: '10px' },
    message: { marginTop: '15px', textAlign: 'center', fontSize: '0.9rem', color: '#fbbf24' },
    title: { textAlign: 'center', color: '#10b981', marginBottom: '20px' },
    row: { display: 'flex', gap: '15px' },
    col: { flex: 1 }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Register</h2>
      <form onSubmit={handleSubmit}>
        <div style={styles.formGroup}>
          <label style={styles.label}>Username</label>
          <input type="text" name="username" value={formData.username} onChange={handleChange} required style={styles.input} />
        </div>
        <div style={styles.formGroup}>
          <label style={styles.label}>Email</label>
          <input type="mail" name="mail" value={formData.mail} onChange={handleChange} required style={styles.input} />
        </div>
        <div style={styles.formGroup}>
          <label style={styles.label}>Password</label>
          <input type="password" name="password" value={formData.password} onChange={handleChange} required style={styles.input} />
        </div>
        <div style={{ ...styles.formGroup, ...styles.row }}>
          <div style={styles.col}>
            <label style={styles.label}>Role</label>
            <select name="rol" value={formData.rol} onChange={handleChange} style={styles.select}>
              <option value="student">Student</option>
              <option value="professor">Professor</option>
            </select>
          </div>
          <div style={styles.col}>
            <label style={styles.label}>Group</label>
            <select name="group" value={formData.group} onChange={handleChange} style={styles.select}>
              <option value="1">Group A (1)</option>
              <option value="2">Group B (2)</option>
              <option value="3">Group C (3)</option>
            </select>
          </div>
        </div>
        <button type="submit" disabled={loading} style={{...styles.button, opacity: loading ? 0.7 : 1}}>
          {loading ? 'Registering...' : 'Register'}
        </button>
      </form>
      {message && <div style={styles.message}>{message}</div>}
      <div style={{textAlign: 'center', marginTop: '15px', fontSize: '0.9rem'}}>
        <a href="/login" style={{color: '#3b82f6', textDecoration: 'none'}}>Already have an account? Login here.</a>
      </div>
    </div>
  );
}

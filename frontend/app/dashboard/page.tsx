'use client';

import { useState, useEffect } from 'react';
import { Upload, FileText, Zap, Activity, Database, Cpu } from 'lucide-react';

export default function Dashboard() {
  const [datasets, setDatasets] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [stats, setStats] = useState({ total_datasets: 0, total_jobs: 0, active_jobs: 0, total_deployments: 0 });
  const [activeTab, setActiveTab] = useState('overview');
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const [datasetsRes, jobsRes, statsRes] = await Promise.all([
        fetch('http://localhost:8002/api/v1/datasets'),
        fetch('http://localhost:8002/api/v1/jobs'),
        fetch('http://localhost:8002/api/v1/admin/stats')
      ]);

      if (datasetsRes.ok) setDatasets(await datasetsRes.json());
      if (jobsRes.ok) setJobs(await jobsRes.json());
      if (statsRes.ok) setStats(await statsRes.json());
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8002/api/v1/datasets/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        alert('Dataset uploaded successfully!');
        fetchData();
      }
    } catch (error) {
      alert('Upload failed: ' + error);
    } finally {
      setUploading(false);
    }
  };

  const startFineTuning = async (datasetId: string) => {
    try {
      const response = await fetch('http://localhost:8002/api/v1/fine-tune', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          dataset_id: datasetId,
          model_name: 'meta-llama/Llama-3.1-8B',
          learning_rate: 0.00002,
          num_epochs: 3,
          batch_size: 4
        })
      });

      if (response.ok) {
        const result = await response.json();
        alert(`Fine-tuning job started! Job ID: ${result.job_id}`);
        fetchData();
      }
    } catch (error) {
      alert('Failed to start fine-tuning: ' + error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                OWN-AI
              </span>
              <span className="ml-4 px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                Dashboard
              </span>
            </div>
            <div className="flex items-center gap-4">
              <a href="/" className="text-gray-600 hover:text-gray-900">← Back to Home</a>
              <a href="http://localhost:8002/docs" target="_blank" className="text-blue-600 hover:text-blue-800">
                API Docs
              </a>
            </div>
          </div>
        </div>
      </header>

      {/* Stats */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Total Datasets</p>
                <p className="text-3xl font-bold text-gray-900">{stats.total_datasets}</p>
              </div>
              <Database className="w-12 h-12 text-blue-500" />
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Total Jobs</p>
                <p className="text-3xl font-bold text-gray-900">{stats.total_jobs}</p>
              </div>
              <Zap className="w-12 h-12 text-purple-500" />
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Active Jobs</p>
                <p className="text-3xl font-bold text-gray-900">{stats.active_jobs}</p>
              </div>
              <Activity className="w-12 h-12 text-green-500" />
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Deployments</p>
                <p className="text-3xl font-bold text-gray-900">{stats.total_deployments || 0}</p>
              </div>
              <Cpu className="w-12 h-12 text-orange-500" />
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow">
          <div className="border-b border-gray-200">
            <nav className="flex -mb-px">
              <button
                onClick={() => setActiveTab('overview')}
                className={`px-6 py-3 text-sm font-medium ${
                  activeTab === 'overview'
                    ? 'border-b-2 border-blue-500 text-blue-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Overview
              </button>
              <button
                onClick={() => setActiveTab('datasets')}
                className={`px-6 py-3 text-sm font-medium ${
                  activeTab === 'datasets'
                    ? 'border-b-2 border-blue-500 text-blue-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Datasets
              </button>
              <button
                onClick={() => setActiveTab('jobs')}
                className={`px-6 py-3 text-sm font-medium ${
                  activeTab === 'jobs'
                    ? 'border-b-2 border-blue-500 text-blue-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Fine-Tuning Jobs
              </button>
            </nav>
          </div>

          <div className="p-6">
            {activeTab === 'overview' && (
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Welcome to OWN-AI Dashboard</h2>
                <p className="text-gray-600 mb-6">
                  Manage your datasets, fine-tune models, and deploy AI without sending data to third parties.
                </p>

                <div className="grid md:grid-cols-2 gap-6">
                  <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-500 transition-colors">
                    <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">Upload Dataset</h3>
                    <p className="text-gray-600 mb-4">Upload your training data to get started</p>
                    <label className="inline-block cursor-pointer bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700">
                      {uploading ? 'Uploading...' : 'Choose File'}
                      <input
                        type="file"
                        className="hidden"
                        accept=".jsonl,.txt,.csv"
                        onChange={handleFileUpload}
                        disabled={uploading}
                      />
                    </label>
                  </div>

                  <div className="border border-gray-300 rounded-lg p-8">
                    <Zap className="w-12 h-12 text-purple-500 mb-4" />
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">Quick Stats</h3>
                    <ul className="space-y-2 text-gray-600">
                      <li>• {datasets.length} dataset{datasets.length !== 1 ? 's' : ''} uploaded</li>
                      <li>• {jobs.length} training job{jobs.length !== 1 ? 's' : ''} created</li>
                      <li>• {stats.active_jobs} job{stats.active_jobs !== 1 ? 's' : ''} currently running</li>
                    </ul>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'datasets' && (
              <div>
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-2xl font-bold text-gray-900">Datasets</h2>
                  <label className="cursor-pointer bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                    {uploading ? 'Uploading...' : '+ Upload Dataset'}
                    <input
                      type="file"
                      className="hidden"
                      accept=".jsonl,.txt,.csv"
                      onChange={handleFileUpload}
                      disabled={uploading}
                    />
                  </label>
                </div>

                {datasets.length === 0 ? (
                  <div className="text-center py-12">
                    <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                    <p className="text-gray-500">No datasets uploaded yet</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {datasets.map((dataset: any) => (
                      <div key={dataset.dataset_id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <h3 className="font-semibold text-gray-900">{dataset.filename}</h3>
                            <p className="text-sm text-gray-500">ID: {dataset.dataset_id}</p>
                            <p className="text-sm text-gray-500">
                              Size: {(dataset.size_bytes / 1024).toFixed(2)} KB
                            </p>
                            <p className="text-sm text-gray-500">
                              Uploaded: {new Date(dataset.uploaded_at).toLocaleString()}
                            </p>
                          </div>
                          <div className="flex gap-2">
                            <button
                              onClick={() => startFineTuning(dataset.dataset_id)}
                              className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 text-sm"
                            >
                              Start Fine-Tuning
                            </button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {activeTab === 'jobs' && (
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Fine-Tuning Jobs</h2>

                {jobs.length === 0 ? (
                  <div className="text-center py-12">
                    <Zap className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                    <p className="text-gray-500">No training jobs yet</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {jobs.map((job: any) => (
                      <div key={job.job_id} className="border border-gray-200 rounded-lg p-4">
                        <div className="flex justify-between items-start mb-3">
                          <div>
                            <h3 className="font-semibold text-gray-900">Job {job.job_id}</h3>
                            <p className="text-sm text-gray-500">Started: {new Date(job.started_at).toLocaleString()}</p>
                          </div>
                          <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                            job.status === 'completed' ? 'bg-green-100 text-green-800' :
                            job.status === 'running' ? 'bg-blue-100 text-blue-800' :
                            job.status === 'failed' ? 'bg-red-100 text-red-800' :
                            'bg-yellow-100 text-yellow-800'
                          }`}>
                            {job.status}
                          </span>
                        </div>

                        <div className="mb-3">
                          <div className="flex justify-between text-sm mb-1">
                            <span className="text-gray-600">Progress</span>
                            <span className="text-gray-900 font-medium">{job.progress_percent}%</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-blue-600 h-2 rounded-full transition-all"
                              style={{ width: `${job.progress_percent}%` }}
                            ></div>
                          </div>
                        </div>

                        <p className="text-sm text-gray-600">{job.message}</p>
                        {job.error && (
                          <p className="text-sm text-red-600 mt-2">Error: {job.error}</p>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

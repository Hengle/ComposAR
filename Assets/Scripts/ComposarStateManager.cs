﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public enum ComposarMode {
	SetupProject, SetupSequence, Layout, SketchChars, SketchModels
}

public class ComposarStateManager : MonoBehaviour {

	// singleton reference
	public static ComposarStateManager Shared;

	private List<Project> Projects;
	private Project CurrentProject;
	private string CurrentSceneName;
	private ComposarMode CurrentMode;

	/* Lifecycle */

	void Awake () {
		ComposarStateManager.Shared = this;
		this.Projects = new List<Project>();
	}

	void Start() {
		// Default to Project scene
		this.ChangeScene("Project");

		// TMP test
		// StartCoroutine(DelayStartSceneIE());
	}

	// TMP
	private IEnumerator DelayStartSceneIE() {
		yield return new WaitForSeconds(2.0f);
		this.ChangeScene("Layout");
	}

	/* Projects */

	public void AddProject(Project project) {
		this.Projects.Add(project);
	}

	public void RemoveProject(Project project) {
		this.Projects.Remove(project);
	}

	public List<Project> GetProjects() {
		return this.Projects;
	}

	public Project GetCurrentProject() {
		return this.CurrentProject;
	}

	public void SetCurrentProject(Project project) {
		this.CurrentProject = project;
	}

	/* Scenes */

	protected void ChangeScene(string sceneName) {
		// Unload existing scene (if there is one)
		if (this.CurrentSceneName != null) {
			SceneManager.UnloadSceneAsync(this.CurrentSceneName);
			
			// Handle Teleportal AR
			if (this.CurrentSceneName == "Layout") {
				SceneManager.UnloadSceneAsync("Teleportal");
			}
			
		}
		
		// Load a new one
		SceneManager.LoadScene(sceneName, LoadSceneMode.Additive);
		this.CurrentSceneName = sceneName;
	}
	
	public ComposarMode GetMode() {
		return this.CurrentMode;
	}

	public void SetMode(ComposarMode mode) {
		switch (mode) {
			case ComposarMode.SetupProject:
				this.ChangeScene("Project");
				break;
			case ComposarMode.SetupSequence:
				this.ChangeScene("Sequence");
				break;
			case ComposarMode.Layout:
				this.ChangeScene("Layout");
				break;
			case ComposarMode.SketchChars:
				this.ChangeScene("SketchAI");
				break;
			case ComposarMode.SketchModels:
				this.ChangeScene("SketchAI");
				break;
		}
	}

}
